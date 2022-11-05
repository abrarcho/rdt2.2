# COMP3670 Lab3
Abrar Chowdhury
-- main.py and network.py implemented entirely by University of Windsor

receiver.py and sender.py simulates RDT2.1, an alternating sequence bit protocol: 0 and 1

## Sender Side Pseudocode
Class RDTSender(message, network_server)
{
    current_sequence = 0
    network = network_server

    def RDT_Send(message)
    {
        for (int i = 0; i < message.length; i++)
        {
            print("Sender expecting sequence number: ", current_sequence)

            int checksum = acsii of message[i]
            packet = RDTSender.make_packet(current_sequence, message[i], checksum)
            print("Sender sending: ", packet)

            reply = network.UDTSend(packet)

            if RDTSender.is_not_expected_seq(reply) == True:
                while RDTSender.is_not_expected_sequence(current_sequence):
                    if RDTSender.is_corrupted(reply):
                        print("Network layer corruption occurred: ", reply)

                    print("Sender re-sending: ", packet)
                    reply = network.UDTSend(packet)

                    print("Sender received: ", packet)

            else if RDTSender.is_not_expected_sequence(reply) == False:
                print("Sender received: ", packet)

            RDTSender.switch_sequence()
        }

        print("Sender done!")
        return
    }

    def switch_sequence()
    {
        if current_sequence == 0:
            current_sequence = 1

        else if current_sequence == 1:
            current_sequence = 0
    }

    def make_packet(sequence, data, checksum)
    {
        reply_packet = 
        {
            'sequence_number' = sequence
            'data' = data
            'checksum' = checksum
        }

        return reply_packet
    }

    def is_not_expected_sequence(reply):
    {
        if reply['sequence_number'] != current_sequence:
            return True
        
        else:
            return False
    }

    def is_corrupted(reply):
        if reply['data'] != char(reply['checksum']):
            return True
        
        elif received_packet['sequence_number']  != 0 and received_packet['sequence_number']  != 1:
            return True

        else:
            return False
}

## Receiver Side Pseudocode

Class RDTReceiver(received_packet)
{
    buffer = list()

    current_sequence = 0

    def RDT_Receive(buffer)
        print("Sender expecting sequence number: ", current_sequence)
        previous_sequence = previous_sequence(current_sequence)

        if is_corrupted(received_packet)
        {
            reply_packet = RDTReceiver.make_reply_packet(previous_sequence, acsii of previous_sequence)
            print('Receiver: reply with: ', reply_packet)

            return reply_packet
        }

        else if is_not_expected_sequence(received_packet)
        {
            reply_packet = RDTReceiver.make_reply_packet(current_sequence, acsii of current_sequence)
            print('Receiver: reply with: ', reply_packet)

            return reply_packet
        }

        else
        {
            buffer.append(received_packet)
            reply_packet = RDTReceiver.make_reply_packet(current_sequence, acsii of current_sequence)
            print('Receiver: reply with: ', reply_packet)
            switch_sequence()

            return reply_packet
        }

    def switch_sequence()
    {
        if current_sequence == 0:
            current_sequence = 1

        else if current_sequence == 1:
            current_sequence = 0
    }

    def previous_sequence()
    {
        if current_sequence == 0:
            return 1

        else if current_sequence == 1:
            return 0
    }

    def make_reply_packet(sequence, checksum)
    {
        reply_packet = 
        {
            'ack = sequence
            'checksum' = checksum
        }

        return reply_packet
    }

    def is_not_expected_sequence(received_packet):
    {
        if received_packet['sequence_number'] != current_sequence:
            return True
        
        else:
            return False
    }

    def is_corrupted(rcv_pkt):
        if received_packet['data'] != char(received_packet['checksum']):
            return True
        
        elif received_packet['sequence_number']  != '0' and received_packet['sequence_number']  != '1':
            return True

        else:
            return False
}