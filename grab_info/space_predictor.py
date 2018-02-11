import urllib.request
import threading

#File_Addrs = 'user_data/links/data.project-gxs.com.final/crawled.txt'   # The address of file containing urls
File_Addrs = 'test_links'      # For testing Purpose

# Initialization
List_Of_URLs = []
List_Of_Invalid_URLs = []
Total_Size = 0
Processed_URLs = 0
Times_Looped = 0
Max_retries = 3
Progress = 0

# Preprocessing
with open(File_Addrs,'r') as f: # Loading uls into list for faster access
    List_Of_URLs = list(set(f.read().splitlines()))    # Removing duplicates
    Total_URLs = len(List_Of_URLs)  # Total number of links
    print("Total Number of URLs to process : {}".format(Total_URLs))

Rate = 100/Total_URLs

# Return the given bytes as a human friendly KB, MB, GB, or TB string'
def HumanReadableSize(B):
   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2) # 1,048,576
   GB = float(KB ** 3) # 1,073,741,824
   TB = float(KB ** 4) # 1,099,511,627,776

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)

# Main fuction to gather info about url
def grab_info(url):
    global Total_Size, Processed_URLs, Total_URLs, Progress,Rate  # Accessing global variables
    if url != ' ':      # Ignoring any whitespaces within the list
        try:
            site = urllib.request.urlopen(url)
            Total_Size = Total_Size + site.length
            print("URLs done processing {}/{} file size: {} Progress:{0:.2f}%".format(Processed_URLs, Total_URLs,HumanReadableSize(site.length), Progress))
            Progress += Rate
            Processed_URLs = Processed_URLs + 1
            if Processed_URLs % 10 == 0:    # Display total size every 50 URLs
               print("\n*********Total size: {}********** Current Progress:{0:.2f}%\n".format(HumanReadableSize(Total_Size), Progress))
        except:
           # print("Network Unavailable or Invalid URL")
            List_Of_Invalid_URLs.append(url) # Catch the URLs that were dropped from the processing queue

# Creating a threading list using list and starting all threads
def thread_series_creator(List_Of_URLs):
    global List_Of_Invalid_URLs,Total_URLs
    List_Of_Invalid_URLs = [] # Reset the invalid url list
    start = 0
    weight = end = (Total_URLs%700)
    while True:
        if start > Total_URLs:
            break
        threads = [threading.Thread(target=grab_info, args=(url,))for url in List_Of_URLs[start:end]]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        start = end
        end = end + weight

# Running the list of URLs
thread_series_creator(List_Of_URLs)
# Retrying if 
while len(List_Of_Invalid_URLs) > 0:
    print("\nTotal unprocessed/invalid URLs: {}\n".format(len(List_Of_Invalid_URLs)))
    if Times_Looped < Max_retries:
        print("*******Retrying unprocessed URLs {}/3*******\n".format(Times_Looped))
        thread_series_creator(List_Of_Invalid_URLs)
        Times_Looped += 1
    else:
        break

# Final result
print("******Final Diagnostic Report******")
print("Total no. of URLs: {} Processed URL rate: {}%".format(Total_URLs,int(Progress)))
print("Total no. of Invalid URLs: {}".format(len(List_Of_Invalid_URLs)))
print("Total size of {}/{} links is: {}".format(Processed_URLs,Total_URLs,HumanReadableSize(Total_Size))) 