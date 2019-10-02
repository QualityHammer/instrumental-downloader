class Logger:

    def __init__(self, song_titles=None):
        if song_titles is None:
            song_titles = []
        self.elapsed = 0
        self.song_count = 0
        self.file_names = []
        self.song_titles = song_titles.copy()

    def log_append(self, filename: str, elapsed: float):
        self.song_count += 1
        self.elapsed += elapsed
        self.song_titles.append(filename[:-4])
        self.file_names.append(filename)
        # print(filename, 'finished downloading in', round(elapsed, 4), 'seconds')

    def hook(self, download):
        if download['status'] == 'finished':
            self.log_append(download['filename'], download['elapsed'])

    def print_log(self):
        print('Downloading', self.song_count, 'songs took', self.elapsed, 'seconds.')
        with open('../log/download_list.txt', 'w+') as file:
            for i in range(len(self.file_names)):
                file.write(self.song_titles[i] + ' as: ' + self.file_names[i] + '\n')

    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)
