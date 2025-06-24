from bing_image_downloader import downloader

downloader.download("tom holland as peter parker in avengers", limit=40,  output_dir='dataset/Train', 
                    adult_filter_off=True, force_replace=False, timeout=60)

