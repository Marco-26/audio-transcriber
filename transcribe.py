import os
from openai import OpenAI
from pydub import AudioSegment

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#TODO: Implement a inbuilt audio compressor
def transcribe_audio(chunk_files):
    num_chunks = len(chunk_files)
    if num_chunks == 0:
        return

    print("Starting transcription")

    transcripted_chunks = ""

    for i in range(num_chunks):
        with open(chunk_files[i], "rb") as audio_to_transcribe:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_to_transcribe,
        )
        print(f"Finished transcribing {i} chunks/s")
        transcripted_chunks += transcript.text
        
    print("Finished transcription")

    return transcripted_chunks;

def split_audio(file_path):
    print("Splitting audio into smaller chunks")
    audio = AudioSegment.from_mp3(file_path)
    max_chunk_length = 25

    total_duration = len(audio) / 1000 
    duration_minutes = total_duration / 60
    
    num_chunks = round(duration_minutes / max_chunk_length)
    chunk_duration = total_duration / num_chunks

    chunks = []
    start_time = 0
    for i in range(num_chunks):
        end_time = start_time + chunk_duration
        chunk = audio[int(start_time * 1000):int(end_time * 1000)]
        chunks.append(chunk)
        start_time = end_time

    print("Done splitting the audio...")

    return chunks

def generate_chunk_files(chunks):
    print("Generating temporary chunk files...")
    chunk_files = []

    for i, chunk in enumerate(chunks):
        temp_file_path = os.path.join("output_chunks", f"chunk_{i}.mp3")
        chunk.export(temp_file_path, format="mp3")
        chunk_files.append(temp_file_path)
    
    print(f"Created {len(chunk_files)} chunks from the original audio")

    return chunk_files

def save_transcript(transcript):
    output_file_path = "transcript.txt"

    with open(output_file_path, "w") as output_file:
        output_file.write(transcript)

    print(f"Transcript saved to {output_file_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage:7 {} <audio_file_path>".format(sys.argv[0]))
        sys.exit(1)

    audio_file_path = sys.argv[1]

    if not os.path.isfile(audio_file_path):
        print("Error: File not found.")
        sys.exit(1)
    
    chunks = split_audio(audio_file_path)
    chunk_files = generate_chunk_files(chunks)

    transcript = transcribe_audio(chunk_files)
    save_transcript(transcript)