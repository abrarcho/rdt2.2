class ReceiverProcess:
    """ Represent the receiver process in the application layer  """
    __buffer = list()

    @staticmethod
    def deliver_data(data):
        """ deliver data from the transport layer RDT receiver to the application layer
        :param data: a character received by the RDT RDT receiver
        :return: no return value
        """
        ReceiverProcess.__buffer.append(data)
        return

    @staticmethod
    def get_buffer():
        """ To get the message the process received over the network
        :return:  a python list of characters represent the incoming message
        """
        return ReceiverProcess.__buffer


class RDTReceiver:
    """" Implement the Reliable Data Transfer Protocol V2.2 Receiver Side """

    def __init__(self):
        self.sequence = '0'

    @staticmethod
    def is_corrupted(rcv_pkt):
        """ Check if the received packet from sender is corrupted or not
            :param packet: a python dictionary represent a packet received from the sender
            :return: True -> if the reply is corrupted | False ->  if the reply is NOT corrupted
        """
        # TODO provide your own implementation
        if rcv_pkt['data'] != chr(rcv_pkt['checksum']):
            return True
        
        elif rcv_pkt['sequence_number'] != '0' and rcv_pkt['sequence_number'] != '1':
            return True

        else:
            return False

    @staticmethod
    def is_not_expected_seq(rcv_pkt, exp_seq):
        """ Check if the received reply from receiver has the expected sequence number
         :param rcv_pkt: a python dictionary represent a packet received by the receiver
         :param exp_seq: the receiver expected sequence number '0' or '1' represented as a character
         :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        # TODO provide your own implementation
        if rcv_pkt['sequence_number'] != exp_seq:
            return True
        
        else:
            return False


    @staticmethod
    def make_reply_pkt(seq, checksum):
        """ Create a reply (feedback) packet with to acknowledge the received packet
        :param seq: the sequence number '0' or '1' to be acknowledged
        :param checksum: the checksum of the ack the receiver will send to the sender
        :return:  a python dictionary represent a reply (acknowledgement)  packet
        """
        reply_pck = {
            'ack': seq,
            'checksum': checksum
        }
        return reply_pck

    @staticmethod
    def switch_sequence(self):
        """Switch the alternating sequence bit"""
        if self.sequence == '0':
            self.sequence = '1'
            
        elif self.sequence == '1':
            self.sequence = '0'

    def previous_seq(self):
        if self.sequence == '0':
            return '1'

        elif self.sequence == '1':
            return '0'

    def rdt_rcv(self, rcv_pkt):
        """  Implement the RDT v2.2 for the receiver
        :param rcv_pkt: a packet delivered by the network layer 'udt_send()' to the receiver
        :return: the reply packet
        """
 
        # deliver the data to the process in the application layer
        print('Receiver: expecting seq num: ', self.sequence)

        previous_seq = RDTReceiver.previous_seq(self)

        if RDTReceiver.is_corrupted(rcv_pkt):
            reply_pkt = RDTReceiver.make_reply_pkt(previous_seq, int(ord(previous_seq)))
            print('Receiver: reply with: ', reply_pkt)

            return reply_pkt

        elif RDTReceiver.is_not_expected_seq(rcv_pkt, self.sequence):
            reply_pkt = RDTReceiver.make_reply_pkt(self.sequence, int(ord(self.sequence)))
            print('Receiver: reply with: ', reply_pkt)

            return reply_pkt

        else:
            ReceiverProcess.deliver_data(rcv_pkt['data'])
            reply_pkt = RDTReceiver.make_reply_pkt(self.sequence, int(ord(self.sequence)))
            print('Receiver: reply with: ', reply_pkt)
            RDTReceiver.switch_sequence(self)
            
            return reply_pkt