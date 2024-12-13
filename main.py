import cv2
import os
from tqdm import tqdm


def get_next_run_number(runs_dir, video_base_name, containing_folder_name):
    """
    Determines the next run number for a given video based on existing runs.

    Parameters:
    - runs_dir (str): Path to the 'runs' directory.
    - video_base_name (str): Base name of the video file (without extension).
    - containing_folder_name (str): Name of the video file's containing folder.

    Returns:
    - int: The next run number.
    """
    # Construct the prefix for run folders
    run_prefix = f"{video_base_name}_{containing_folder_name}_run"

    # List all existing run folders that start with the run_prefix
    existing_runs = [
        folder for folder in os.listdir(runs_dir)
        if os.path.isdir(os.path.join(runs_dir, folder)) and folder.startswith(run_prefix)
    ]

    run_numbers = []
    for run in existing_runs:
        # Extract the run number from the folder name
        parts = run.split(run_prefix)
        if len(parts) == 2 and parts[1].isdigit():
            run_numbers.append(int(parts[1]))

    if run_numbers:
        return max(run_numbers) + 1
    else:
        return 1


def extract_frames(video_path, output_folder, frame_interval=10):
    """
    Extracts every nth frame from a video and saves them as PNG images.

    Parameters:
    - video_path (str): Path to the input video file.
    - output_folder (str): Directory where extracted frames will be saved.
    - frame_interval (int): Interval of frames to extract (e.g., every 10th frame).
    """

    # Check if the video file exists
    if not os.path.isfile(video_path):
        print(f"Error: Video file '{video_path}' does not exist.")
        return

    # Check if the output folder exists; if not, create it
    if not os.path.exists(output_folder):
        try:
            os.makedirs(output_folder)
            print(f"Created output folder: {output_folder}")
        except Exception as e:
            print(f"Error creating output folder '{output_folder}': {e}")
            return
    else:
        print(f"Output folder already exists: {output_folder}")

    # Initialize video capture
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Cannot open video file '{video_path}'.")
        return

    frame_count = 0  # Total number of frames processed
    saved_count = 0  # Number of frames saved

    # Get total number of frames for progress bar
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) if cap.get(cv2.CAP_PROP_FPS) > 0 else 30  # Default FPS if unavailable

    print(f"Starting frame extraction from '{video_path}' with an interval of every {frame_interval} frames.")

    try:
        # Initialize progress bar
        with tqdm(total=total_frames, desc="Extracting frames", unit="frame") as pbar:
            while True:
                ret, frame = cap.read()

                if not ret:
                    break

                if frame_count % frame_interval == 0:
                    frame_filename = os.path.join(output_folder, f"frame_{frame_count:06d}.png")
                    try:
                        cv2.imwrite(frame_filename, frame)
                        saved_count += 1
                    except Exception as e:
                        print(f"Error saving frame {frame_count}: {e}")

                frame_count += 1
                pbar.update(1)
    except KeyboardInterrupt:
        print("\nExtraction interrupted by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        # Release resources
        cap.release()
        print("\nFinished processing.")
        print(f"Total frames processed: {frame_count}")
        print(f"Total frames saved: {saved_count}")


def main():
    # === USER CONFIGURATION START ===

    # Specify the path to your input video file
    # Example for Windows: "C:/Users/YourName/Videos/classroom_video.mp4"
    # Example for macOS/Linux: "/Users/YourName/Videos/classroom_video.mp4"
    video_path = "Videos/My Project/Zoom.mp4"  # <-- Update this path

    # (Optional) Specify the frame interval (default is every 10th frame)
    frame_interval = 10

    # === USER CONFIGURATION END ===

    # Determine the directory where main.py is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the 'runs' directory within the project directory
    runs_dir = os.path.join(script_dir, "runs")

    # Ensure the 'runs' directory exists
    if not os.path.exists(runs_dir):
        try:
            os.makedirs(runs_dir)
            print(f"Created 'runs' directory at: {runs_dir}")
        except Exception as e:
            print(f"Error creating 'runs' directory '{runs_dir}': {e}")
            return
    else:
        print(f"'runs' directory already exists at: {runs_dir}")

    # Extract the base name of the video file (without extension)
    video_base_name = os.path.splitext(os.path.basename(video_path))[0]

    # Extract the name of the video file's containing folder
    containing_folder_path = os.path.dirname(video_path)
    containing_folder_name = os.path.basename(containing_folder_path)

    # Determine the next run number
    run_number = get_next_run_number(runs_dir, video_base_name, containing_folder_name)

    # Define the run-specific directory name (e.g., classroom_video_Videos_run1)
    run_dir_name = f"{video_base_name}_{containing_folder_name}_run{run_number}"

    # Define the full path to the run-specific directory
    run_dir = os.path.join(runs_dir, run_dir_name)

    # Define the 'extracted_frames' directory within the run-specific directory
    extracted_frames_dir = os.path.join(run_dir, "extracted_frames")

    # Create the run-specific directory and 'extracted_frames' subdirectory
    if not os.path.exists(extracted_frames_dir):
        try:
            os.makedirs(extracted_frames_dir)
            print(f"Created run directory: {run_dir}")
            print(f"Created 'extracted_frames' directory: {extracted_frames_dir}")
        except Exception as e:
            print(f"Error creating run directories: {e}")
            return
    else:
        print(f"'extracted_frames' directory already exists: {extracted_frames_dir}")

    # Start frame extraction
    extract_frames(video_path, extracted_frames_dir, frame_interval)


if __name__ == "__main__":
    main()
