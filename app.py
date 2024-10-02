from flask import Flask, render_template, request, redirect, url_for, session
import os
import yt_dlp  # Ensure yt-dlp is installed
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for using session

# Function to download the YouTube video
def download_video(url):
    try:
        # Simulate a delay to represent download time
        time.sleep(5)

        # Set up YouTube download options
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save location
            'format': 'best',  # Choose the best available format
        }

        # Download the video using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "Video download successful!"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def home():
    # Ensure the session data is cleared when visiting the home page
    session.pop('download_result', None)  # Clear any old session data

    if request.method == 'POST':
        # Get the YouTube URL from the form and store it in the session
        youtube_url = request.form.get('input_value')
        session['youtube_url'] = youtube_url

        # Redirect to the waiting page before starting the download
        return redirect(url_for('wait'))

    return render_template('index.html')

@app.route('/wait')
def wait():
    # Render a wait page
    return render_template('wait.html')

@app.route('/process_download')
def process_download():
    # Get the YouTube URL from the session
    youtube_url = session.get('youtube_url')

    if youtube_url:
        # Call the function to download the video and store the result in the session
        download_result = download_video(youtube_url)
        session['download_result'] = download_result

        # After processing, redirect to the result page
        return redirect(url_for('result'))
    else:
        return redirect(url_for('home'))

@app.route('/result')
def result():
    # Get the result from the session
    result_message = session.pop('download_result', None)

    if result_message is None:
        # If there's no result message, redirect back to the home page
        return redirect(url_for('home'))

    return render_template('result.html', result=result_message)

if __name__ == '__main__':
    # Create downloads directory if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    app.run(debug=True)

