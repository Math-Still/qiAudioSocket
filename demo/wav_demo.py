import socket
import time
import wave

# Audio parameters
channels = 1  # Mono
sample_rate = 16000  # Sample rate
buffer_size = 170  # Buffer size (in milliseconds)

# Calculate the number of samples
num_samples = int(sample_rate * (buffer_size / 1000))

# Create empty audio data

# Create a WAV file stream

HOST = ''
PORT = 12345
buffer_size = 1365 * 2
# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
count = 0
client_socket.sendall(b'1')
time.sleep(1)


print("connected")
# Send and receive data
while count <= 3000:
    data = count
    response = client_socket.recv(buffer_size)
    audio_data = response
    count += 1
    with wave.open('a{}.wav'.format(count), 'w') as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data)
    # Generate test WAV stream
client_socket.sendall(b'2')
client_socket.close()