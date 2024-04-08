from transformers import pipeline
from YTextract import youtubeCaptionExtractor
import socket
import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import os


# summarizer = pipeline('summarization', model='sshleifer/distilbart-cnn-12-6')


# summarizer = pipeline('summarization', model='t5-small', tokenizer='t5-small')

#
# def SummaryOfVideo(video_links):
#     transcript_text = youtubeCaptionExtractor(video_links)
#
#     if transcript_text == -1:
#         return "Error: Retry Again or Check for Subtitle!!"
#     elif transcript_text == -2:
#         return "Error: Invalid Link!!"
#
#     num_iters = int(len(transcript_text) / 1000)
#     summarized_text = []
#
#     for i in range(0, num_iters + 1):
#         start = 0
#         start = i * 1000
#         end = (i + 1) * 1000
#         #   print("input text \n" + transcript_text[start:end])
#         out = summarizer(transcript_text[start:end], length_penalty=2.0, max_length=90, min_length=10)
#         out = out[0]
#         out = out['summary_text']
#         #   print("Summarized text\n"+out)
#         summarized_text.append(out)
#     return [summarized_text,len(summarized_text[0]), len(transcript_text)  ]
#     # print(summarized_text)
#     # print(len(summarized_text[0]), len(transcript_text))

def gpt3_summarizer(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can choose other engines if needed
        prompt=prompt,
        max_tokens=150,  # Adjust the max tokens as per your requirement
        temperature=0.7  # Adjust temperature for randomness in outputs
    )
    return response.choices[0].text.strip()


llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8)


def DirectQuestionAnswer(Transcript_text):
    """Direct Question and Answer"""

    prompt_template = PromptTemplate(
        input_variables=["Transcript"],
        template="""Provide a brief summary of the YouTube video's content, focusing on detailed explanations of specific events while maintaining a concise and informative style. 
        Directly reference characters and events, avoiding indirect language. Ensure the summary aligns with the video's tone and style.
        Capture the essence of the video's context, correcting any grammatical errors, improving readability, and eliminating unnecessary nuances or informal language. 
        Additionally, ensure that the resulting summary is informative and aligns with the tone and style maintained by the characters throughout the video. ,
        Transcript: {Transcript},
        """
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)

    output = chain.run(Transcript=Transcript_text)
    print(output)
    return output


def SummaryOfVideo(video_links):
    transcript_text = youtubeCaptionExtractor(video_links)
    print(f"Transcript Text: {transcript_text}", end="\n\n\n")

    if transcript_text == -1:
        return ["Error: Retry Again or Check for Subtitle!!", 0, 0]
    elif transcript_text == -2:
        return ["Error: Invalid Link!!", 0, 0]
    else:
        summarized_text = DirectQuestionAnswer(transcript_text)

        return [summarized_text, len(summarized_text), len(transcript_text)]


# if __name__ == "__main__":
def init():
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to a specific address and port
    server_address = ('localhost', 1240)
    server_socket.bind(server_address)

    print(f"UDP server listening on {server_address}")

    while True:
        print("Waiting for a message...")
        video_link, client_address = server_socket.recvfrom(1024)
        summary, length_of_summary, length_of_transcript = SummaryOfVideo(video_link.decode())
        print(f"Received message from {client_address}: {video_link.decode()}")
        response = ' '.join(summary)
        # response = Summary_of_video
        # server_socket.sendto(summary.encode(), client_address)
        if isinstance(response, str):
            server_socket.sendto(response.encode(), client_address)
            server_socket.sendto(str(length_of_summary).encode(), client_address)
            server_socket.sendto(str(length_of_transcript).encode(), client_address)
        else:
            print("Response is not a string.")
