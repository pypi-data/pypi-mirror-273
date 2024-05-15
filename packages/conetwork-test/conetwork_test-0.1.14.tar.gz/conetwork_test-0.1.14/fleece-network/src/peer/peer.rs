use std::time::Duration;

use bytes::Bytes;
use libp2p::{identity, swarm, Multiaddr, PeerId, Swarm};
use tokio::sync::{mpsc, oneshot};
use tower::Service;

use crate::{error::Error, router::Router, transport::TransportBuilder};

use super::{
    behaviour::Behaviour,
    codec,
    eventloop::{Command, Event, EventLoop},
    handler::Handler,
};

pub struct Peer {
    pub peer_id: PeerId,

    eventloop: EventLoop,

    router:
        Router<codec::Request, codec::Response, Error, Handler<codec::Request, codec::Response>>,

    event_rx: mpsc::Receiver<Event>,
    pub command_tx: mpsc::Sender<Command>,
}

impl Peer {
    pub fn new(
        center_addr: Multiaddr,
        center_peer_id: PeerId,
        self_addr: Multiaddr,
        handler: Handler<codec::Request, codec::Response>,
    ) -> Self {
        let keypair = identity::Keypair::generate_ed25519();
        let peer_id = keypair.public().to_peer_id();
        let transport_builder = TransportBuilder::new(keypair.clone())
            .with_tcp()
            .with_ws()
            .with_quic();
        let (transport_builder, relay_behaviour) = transport_builder.with_relay();
        let transport = transport_builder.build();
        let behaviour = Behaviour::new(&keypair, relay_behaviour);
        let swarm_config = swarm::Config::with_tokio_executor()
            .with_idle_connection_timeout(Duration::from_secs(600));
        let mut swarm = Swarm::new(transport, behaviour, peer_id.clone(), swarm_config);

        // setup for direct connection
        swarm.listen_on(self_addr.clone()).unwrap();

        // setup for stream

        let (command_tx, command_rx) = mpsc::channel(32);
        let (event_tx, event_rx) = mpsc::channel(32);
        let eventloop = EventLoop::new(
            swarm,
            command_tx.clone(),
            command_rx,
            event_tx,
            center_addr.clone(),
            center_peer_id.clone(),
        );

        Self {
            peer_id,
            eventloop,
            router: Router::new(handler),
            event_rx,
            command_tx,
        }
    }

    pub async fn run(mut self) {
        tokio::spawn(self.eventloop.run());
        loop {
            match self.event_rx.recv().await {
                Some(event) => match event {
                    Event::Request {
                        peer_id,
                        request_id,
                        request,
                    } => {
                        let future = self.router.call(request);
                        let command_tx = self.command_tx.clone();
                        tokio::spawn(async move {
                            let response = future.await;
                            let (sender, receiver) = oneshot::channel();
                            if response.is_err() {
                                command_tx
                                    .send(Command::Response {
                                        peer_id,
                                        request_id,
                                        response: codec::Response::new(
                                            String::from("error"),
                                            Bytes::default(),
                                        ),
                                        sender,
                                    })
                                    .await
                                    .unwrap();
                            } else {
                                command_tx
                                    .send(Command::Response {
                                        peer_id,
                                        request_id,
                                        response: response.unwrap(),
                                        sender,
                                    })
                                    .await
                                    .unwrap();
                            }
                            receiver.await.unwrap().unwrap();
                        });
                    }
                },
                None => break,
            }
        }
    }
}
