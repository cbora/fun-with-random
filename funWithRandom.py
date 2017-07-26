
# coding: utf-8

# In[ ]:

import requests
import time
from PIL import Image
import numpy as np
import wave


# ## Create RGB BITMAP of 128 pixels by 128 pixels
# Another comment

# In[ ]:

def has_quota():
    """
        Checks for quota
        returns True if still has quota else False
    """
    url = "https://www.random.org/quota/?format=plain"
    response = requests.get(url)
    if response.status_code == 200:
        return response.content.split() >= 0
    return False


# In[ ]:

def chunk_requests(count, min, max):
    """
        Chunks requests 
        checks whether the max
        returns list of numbers
    """
    # make the url
    numbers_url = "https://www.random.org/integers/?num={}&min={}&max={}&col=3&base=10&format=plain&rnd=new".format(count, min, max)
    # make the requests on the API
    if not has_quota():
        # if no quota available sleep for ten minutes
        time.sleep(60*10)
    numbers_response = requests.get(numbers_url, timeout=60*10)
    # return the processed list of numbers if successful
    if numbers_response.status_code == 200:
        return numbers_response.content.split()
    print "Failed request with code: ", numbers_response.status_code
    return []


# In[ ]:

def generate_numbers(count, min, max):
    """
    Generates numbers by calling chunk requests
    """
    max_count = 1000
    if count <= max_count:
        # if the requested count is less than max
        return chunk_requests(count, min, max)
    
    results = []
    while count > 0:
        # Now process the count in chunks
        if count <= max_count:
            # if count is close to max_count
            this_count = count
            count = -1
        else:
            # count is far greater than max_count
            this_count = max_count
            count -= max_count
        results = results + chunk_requests(this_count, min, max)
    return results


# In[ ]:

# generate n pixels = 128 by 128
# RGB has 3 values so we multiply by 3
n_pixels = 128*128*3
# generate numbers using the API
min = 0
max = 255
numbers = generate_numbers(n_pixels, min, max)


# In[ ]:

WIDTH=128
HEIGHT=128
img = Image.new(WIDTH, HEIGHT, 'RGB')


# In[ ]:

# convert to numpy array
np_arr = np.asarray(numbers).reshape((128, 128, 3))


# In[ ]:

im = Image.fromarray(np_arr.astype('uint8')).convert('RGBA')


# In[ ]:

im.show()


# ## A white noise WAV sound sample of 3 second

# In[ ]:

# Generate a 16-bit PCM audio in the range of -32767, 32767
noise_min = -32767
noise_max = 32767
noise_count = 44100*3 # for 3 seconds


# In[ ]:

# Get the random numbers
noise = generate_numbers(noise_count, noise_min, noise_max)
noise = map(int, noise) # convert to integers


# In[ ]:

# Generate white noise using python libraries
# reference to https://soledadpenades.com/2009/10/29/fastest-way-to-generate-wav-files-in-python-using-the-wave-module/
noise_output = wave.open('noise.wav', 'w')
noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
for i in range(0, noise_count):
        value = noise[i]
        packed_value = struct.pack('h', value)
        noise_output.writeframes(packed_value)
        noise_output.writeframes(packed_value)

noise_output.close()


# ## RSA Key pair

# In[ ]:



