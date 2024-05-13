from venv import logger
from dalpha.message_consumer import KafkaMessageConsumer
from dalpha.slack import slack_alert

class UpdateAgent:
    def __init__(self):
        self.message_consumer = KafkaMessageConsumer(api_id=0, kafka_topic="update")
    
    def poll(self):
        '''
        data update의 경우 kafka로부터 data update event가 담긴 메세지를 받아온다.
        '''
        ret = self.message_consumer.poll()

        if len(ret) == 0:
            return None
        elif len(ret) == 1:
            logger.info(
                message = f"return kafka item: {ret[0]}",
                event = Event.POLL,
                data = ret[0]
            )
            self.poll_time = time.time()
            return ret[0]
        else:
            logger.info(
                message = f"return kafka item: {ret}",
                event = Event.POLL,
                data = ret
            )
            self.poll_time = time.time()
            return ret
        
    def validate(self, output={}, alert = False):
        '''
        data update 파이프라인에서의 validate이라고 보면 된다.
        update가 끝난뒤 이 함수를 통해서 kafka의 offset을 commit한다.
        원한다면 slack alert를 보낼 수 있다.
        '''
        self.message_consumer.commit()
        logger.info(
            message = "update_complete payload",
            event = Event.VALIDATE,
            data = output
        )
        if alert:
            slack_alert(
                '#alert_data_update',
                f"update_complete payload for topic: {self.kafka_topic} - result: {output}"
            )
        

    def validate_error(self, output={}, alert = False):
        '''
        data update 파이프라인에서의 validate_error이라고 보면 된다.
        update 도중 에러가 발생했을 때 이 함수를 통해서 kafka의 offset을 commit한다.
        원한다면 slack alert를 보낼 수 있다.
        '''
        self.message_consumer.commit()
        logger.info(
            message = "update_error payload",
            event = Event.VALIDATE_ERROR,
            data = output
        )
        if alert:
            slack_alert(
                '#alert_data_update',
                f"update_error payload for topic: {self.kafka_topic} - result: {output}"
            )
