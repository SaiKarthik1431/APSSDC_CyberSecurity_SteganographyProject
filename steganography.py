#!/usr/bin/env python
# coding: utf-8

# In[5]:


import piexif
import os
import shutil

def duplicate_image_file(original_image_file):
    try:
        # Check if the image file exists
        if not os.path.isfile(original_image_file):
            raise FileNotFoundError(f"The file '{original_image_file}' does not exist.")
        
        # Create a new file name for the duplicate image
        duplicate_image_file = f"{os.path.splitext(original_image_file)[0]}_encrypted.jpg"
        
        # Copy the original image file to the new duplicate image file
        shutil.copyfile(original_image_file, duplicate_image_file)
        
        return duplicate_image_file
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def encode_text_in_metadata(image_file, text):
    try:
        # Create a duplicate image file
        duplicate_file = duplicate_image_file(image_file)
        
        if not duplicate_file:
            raise Exception(f"Failed to create a duplicate of '{image_file}'.")
        
        # Load EXIF data from the duplicate image file
        exif_dict = piexif.load(duplicate_file)
        
        # Convert text to bytes
        encoded_text = text.encode('utf-8')
        
        # Encode the text into the 'UserComment' tag of EXIF
        exif_dict['Exif'][piexif.ExifIFD.UserComment] = encoded_text
        
        # Convert modified EXIF data back to bytes
        exif_bytes = piexif.dump(exif_dict)
        
        # Update the duplicate image file with the modified EXIF data
        piexif.insert(exif_bytes, duplicate_file)
        
        print("Text encoded successfully in the metadata of", duplicate_file)
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except PermissionError:
        print(f"Error: Permission denied to access {image_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def decode_text_from_metadata(image_file):
    try:
        # Check if the image file exists
        if not os.path.isfile(image_file):
            raise FileNotFoundError(f"The file '{image_file}' does not exist.")
        
        # Load EXIF data from the image file
        exif_dict = piexif.load(image_file)
        
        # Retrieve encoded text from the 'UserComment' tag of EXIF
        if piexif.ExifIFD.UserComment in exif_dict['Exif']:
            encoded_text = exif_dict['Exif'][piexif.ExifIFD.UserComment]
            decoded_text = encoded_text.decode('utf-8')
            print("Decoded text:", decoded_text)
        else:
            print("No hidden text found in the metadata of", image_file)
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except PermissionError:
        print(f"Error: Permission denied to access {image_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    try:
        image_file = input("Enter the image file with extension: ").strip()
        
        # Validate if the image file path is provided
        if not image_file:
            raise ValueError("Image file path cannot be empty.")
        
        # Check if the image file exists
        if not os.path.isfile(image_file):
            raise FileNotFoundError(f"The file '{image_file}' does not exist.")
        
        choice = input("\n\tList of Choices\n""\t---------------\n""1. Encrypt the secret text in the multimedia image file\n""2. Decrypt the secret text from the encrypted multimedia image file\n""\nEnter Your Choice:").strip()
        
        if choice == '1':
            text_to_hide = input("Enter the text to hide in metadata: ")
            encode_text_in_metadata(image_file, text_to_hide)
        elif choice == '2':
            decode_text_from_metadata(image_file)
        else:
            print("Invalid choice. Please enter 1 or 2.")
    
    except ValueError as ve:
        print(f"Error: {ve}")
    except FileNotFoundError as fe:
        print(f"Error: {fe}")
    except PermissionError:
        print(f"Error: Permission denied to access {image_file}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()


# In[ ]:




