import os
from datasets import load_dataset

def download_and_format_data(output_file="train_data.txt", num_samples=1000):
    """
    Downloads poems and stories from Hugging Face and formats them for training.
    """
    
    data_buffer = []

    print("Downloading Poems from 'merve/poetry'...")
    try:
        # Load poems dataset
        # This dataset usually has 'content', 'author', 'poem name', 'age', 'type'
        poems_ds = load_dataset("merve/poetry", split="train", streaming=True)
        
        count = 0
        for item in poems_ds:
            if count >= num_samples // 2:
                break
            
            # Extract fields
            content = item.get("content", "").strip()
            topic = item.get("type", "General") # Use 'type' as topic (e.g., Love, Nature)
            
            if content and topic:
                formatted_entry = f"Write a poem about {topic}:\n{content}\n\n"
                data_buffer.append(formatted_entry)
                count += 1
                
        print(f"Collected {count} poems.")
        
    except Exception as e:
        print(f"Error downloading poems: {e}")

    print("Downloading Stories from 'ajibawa-2023/Children-Stories-Collection'...")
    try:
        # Load stories dataset
        # Inspecting structure usually reveals 'text', 'title', etc.
        # We'll try to find a title or theme.
        stories_ds = load_dataset("ajibawa-2023/Children-Stories-Collection", split="train", streaming=True)
        
        count = 0
        for item in stories_ds:
            if count >= num_samples // 2:
                break
            
            # This dataset likely has 'text' and maybe 'title'
            # Let's check keys if we fail, but for now assume 'text' exists.
            # If 'title' exists, use it.
            
            text = item.get("text", "")
            title = item.get("title", "")
            
            # If no title, try to extract from text or use generic
            if not title:
                # Some datasets have the title as the first line
                lines = text.split('\n')
                if len(lines) > 0:
                    possible_title = lines[0].strip()
                    if len(possible_title) < 50: # Heuristic
                        title = possible_title
                        text = "\n".join(lines[1:])
                    else:
                        title = "a Story"
            
            if text:
                formatted_entry = f"Story about {title}:\n{text.strip()}\n\n"
                data_buffer.append(formatted_entry)
                count += 1

        print(f"Collected {count} stories.")

    except Exception as e:
        print(f"Error downloading stories: {e}")
        # Fallback to TinyStories if the above fails
        print("Attempting fallback to 'roneneldan/TinyStories'...")
        try:
             ds = load_dataset("roneneldan/TinyStories", split="train", streaming=True)
             count = 0
             for item in ds:
                if count >= 200: break
                text = item.get("text", "").strip()
                if text:
                    formatted_entry = f"Story about a Tiny Story:\n{text}\n\n"
                    data_buffer.append(formatted_entry)
                    count += 1
             print(f"Collected {count} fallback stories.")
        except Exception as e2:
            print(f"Fallback failed: {e2}")

    # Write to file
    if data_buffer:
        print(f"Writing {len(data_buffer)} samples to {output_file}...")
        with open(output_file, "w", encoding="utf-8") as f:
            for entry in data_buffer:
                f.write(entry)
        print("Done!")
    else:
        print("No data collected.")

if __name__ == "__main__":
    download_and_format_data()
