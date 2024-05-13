import ipih

from pih import A, PIHThread
from pih.collections import Message
from MessageQueueService.const import SD
from pih.tools import ParameterList, while_not_do, ne, js, nn, j


SC = A.CT_SC

ISOLATED: bool = True

from collections import defaultdict
from time import sleep
import random


class DH:
    message_buffer_list: dict[str, list[Message]] = defaultdict(list)


def service_call_handler(sc: SC, pl: ParameterList) -> bool | None:
    if sc == SC.add_message_to_queue:
        message: Message | None = pl.next(Message())
        if ne(message):
            message_buffer_list: list[Message] = DH.message_buffer_list[message.sender]
            if pl.next():
                message_buffer_list.insert(0, message)
            else:
                message_buffer_list.append(message)
            return True
    return None


def send_message(message: Message) -> None:
    if ne((message.message or "").strip()):
        recipient: str = A.S_P.test_recipient(message.sender) or message.recipient

        def send() -> bool:
            if nn(message.location):
                return A.ME_WH_W.send_location(
                    recipient, message.location, message.message, message.sender
                )
            if nn(message.image_url):
                return A.ME_WH_W.send_image(
                    recipient,
                    message.message,
                    A.D_CO.file_to_base64(message.image_url),
                    message.sender,
                )
            return A.ME_WH_W.send(recipient, message.message, message.sender)

        while_not_do(send)


def complete_buffered_message_sending_action(message: Message) -> bool:
    A.L.polibase(js(("Сообщение было отправлено аббоненту:", message.recipient)))
    return True


def buffered_messages_sending_thread_action(sender: A.CT_ME_WH_W.Profiles) -> None:
    while True:
        message_buffer_list: list[Message] = DH.message_buffer_list[sender.value]
        if ne(message_buffer_list):
            message: Message | None = None
            try:
                if A.S.get(A.CT_S.WHATSAPP_SENDING_MESSAGES_VIA_WAPPI_IS_ON):
                    message = message_buffer_list.pop(0)
                    send_message(message)
                    delay: int = random.randint(
                        A.S.get(
                            A.CT_S.WHATSAPP_BUFFERED_MESSAGE_MIN_DELAY_IN_MILLISECONDS
                        ),
                        A.S.get(
                            A.CT_S.WHATSAPP_BUFFERED_MESSAGE_MAX_DELAY_IN_MILLISECONDS
                        ),
                    )
                    sleep(delay / 1000)
            except Exception as error:
                A.L.polibase(
                    j(
                        (
                            "Ошибка при отправке сообщенияю аббоненту ",
                            message.recipient,
                            ". Ошибка: ",
                            error,
                        )
                    ),
                    A.CT_L_ME_F.ERROR,
                )
        else:
            sleep(1)


def service_starts_handler() -> None:
    for sender_profile in A.CT_ME_WH_W.Profiles:
        PIHThread(buffered_messages_sending_thread_action, args=(sender_profile,))


def start(as_standalone: bool = False) -> None:
    A.SRV_A.serve(
        SD,
        service_call_handler,
        service_starts_handler,
        isolate=ISOLATED,
        as_standalone=as_standalone,
    )


if __name__ == "__main__":
    start()
