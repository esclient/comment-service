import logging
from ..kafka.producer import ModerationRequestProducer
from ..kafka.consumer import ModerationResponseConsumer
from ..kafka.config import KafkaConfig
from commentservice.grpc import comment_pb2

logger = logging.getLogger(__name__)

class ModerationService:

    def __init__(self):
        self.config = KafkaConfig()

        self.producer = ModerationRequestProducer(self.config)

        self.consumer = ModerationResponseConsumer(
            self.config,
            callback=self._handle_moderation_response
        )

        self.consumer.start()

        logger.info("ModerationService initialized")

    def request_moderaiton(self, comment_id: int, comment_text: str) -> bool:
        try:
            request = comment_pb2.CreateCommentRequest()
            request.id = comment_id
            request.text = comment_text
            
            success = self.producer.send_moderation_request(request)

            if success:
                logger.info(f"Moderation request sent: comment_id={comment_id}")
            else:
                logger.error(f"Failed to send moderation request: comment_id={comment_id}")
            
            return success
        
        except Exception as e:
            logger.error(f"Error requesting moderation: {e}")
            return False

    def _handle_moderation_response(self, response: comment_pb2.CreateCommentResponse, request_id: int):
        
        try:
            is_flagged = response.success

            logger.info(
                f"Moderation result received: comment_id={request_id}, "
                f"flagged={is_flagged}"
            )

            self._update_comment_status(request_id, is_flagged)

        except Exception as e:
            logger.error(f"Error handling moderation response: {e}")
    
    def _update_comment_status(self, comment_id: int, is_flagged: bool):
        # TODO: Implement database update
        # Example:
        # if is_flagged:
        #     db.update_comment_status(comment_id, status='FLAGGED')
        # else:
        #     db.update_comment_status(comment_id, status='APPROVED')
        logger.debug("Testing")
    
    def shutdown(self):
        self.consumer.stop()
        self.producer.flush()
        logger.info("ModerationService shutdown complete")

    