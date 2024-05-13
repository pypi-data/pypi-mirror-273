import argparse
import os

import dotenv
import vertexai
from google.cloud import storage
from vertexai.generative_models import GenerativeModel, Part

dotenv.load_dotenv()


def upload_if_not_exists(local_file_path, bucket_name, upload_path=''):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    file_name = os.path.basename(local_file_path)
    full_blob_name = os.path.join(upload_path, file_name) if upload_path else file_name
    blob = bucket.blob(full_blob_name)

    if blob.exists():
        blob.reload()
        if blob.size == os.path.getsize(local_file_path):
            # print("botrun_vertexai.py, File already exists and is the same size, no upload needed.")
            return f"gs://{bucket_name}/{full_blob_name}"
        else:
            # print("botrun_vertexai.py, File exists but sizes differ, uploading new file.")
            pass
    else:
        # print("File does not exist, uploading new file.")
        pass

    blob.upload_from_filename(local_file_path)
    return f"gs://{bucket_name}/{full_blob_name}"


def get_mime_type(file_uri):
    extension = os.path.splitext(file_uri)[1].lower()
    mime_types = {
        '.mp4': 'video/mp4',
        '.mov': 'video/quicktime',
        '.avi': 'video/x-msvideo',
        '.mkv': 'video/x-matroska',
        '.webm': 'video/webm'
    }
    return mime_types.get(extension, 'application/octet-stream')


def analyze_video(project, location, model_name, video_file_uri, prompt):
    dotenv.load_dotenv()
    vertexai.init(project=project, location=location)
    model = GenerativeModel(model_name=model_name)
    mime_type = get_mime_type(video_file_uri)
    video_file = Part.from_uri(video_file_uri, mime_type=mime_type)
    contents = [video_file, prompt]
    response = model.generate_content(contents, stream=True)
    lst_response = []
    for chunk in response:
        print(chunk.text, end='')
        lst_response.append(chunk.text)
    return "".join(lst_response)


def process_video(project, location, model_name, local_video_path, bucket_name, upload_path, prompt):
    gcs_uri = upload_if_not_exists(local_video_path, bucket_name, upload_path)
    return analyze_video(project, location, model_name, gcs_uri, prompt)


def botrun_gemini(
        local_video_path='users/BOTRUN_FOLDER/video/IMG_0017.MOV',
        prompt="請用繁體中文解析這個影片，"
               "若影片中使用者有提問的話，"
               "請妳詳細貼心的仔細回答該提問（並且舉例），"
               "不能遺漏任何細節，"
               "請妳回答時不要用 markdown 語法，"
               "如果妳有標題想要強調可以用適合該標題的可愛emoji"):
    project = 'plant-hero'
    location = 'us-central1'
    model_name = 'gemini-1.5-pro-preview-0409'
    bucket_name = 'gs_bucket_gemini'
    cleaned_path = local_video_path.replace('./', '')
    upload_path = cleaned_path
    response = process_video(project, location, model_name, local_video_path, bucket_name, upload_path, prompt)
    return response


def main():
    parser = argparse.ArgumentParser(description="Video Content Analysis using Vertex AI")
    parser.add_argument('--project', type=str, default='plant-hero')
    parser.add_argument('--location', type=str, default='us-central1')
    parser.add_argument('--model_name', type=str, default='gemini-1.5-pro-preview-0409')
    parser.add_argument('--local_video_path', type=str, default='users/BOTRUN_FOLDER/video/IMG_0017.MOV')
    parser.add_argument('--bucket_name', type=str, default='gs_bucket_gemini')
    parser.add_argument('--upload_path', type=str, default='users/BOTRUN_FOLDER/video/IMG_0017.MOV')
    parser.add_argument('--prompt', type=str,
                        default="請用繁體中文解析這個影片，若影片中使用者有提問的話，請妳詳細貼心的仔細回答該提問（並且舉例）不能遺漏任何細節")

    args = parser.parse_args()

    response = process_video(args.project, args.location, args.model_name, args.local_video_path, args.bucket_name,
                             args.upload_path, args.prompt)


if __name__ == '__main__':
    main()
