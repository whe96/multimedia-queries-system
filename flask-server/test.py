import random

filenames = ["flowers", "interview", "movie", "musicvideo", "sports", "starcraft", "traffic"]
max_duration = 20
query_duration = 5


def random_start_time():
    start = random.uniform(0, max_duration - query_duration)
    return start


def simulate_similarity(func, num_iters=10):
    self_simis = 0.0
    other_simis = 0.0
    distance = 0.0
    for iter in range(num_iters):
        video1 = random.sample(filenames, 1)[0]
        start1 = random_start_time()

        self_similarity = 0.0
        for _ in range(len(filenames) - 1):
            start2 = random_start_time()
            self_similarity += func(video1, start1, video1, start2)
        self_similarity /= len(filenames) - 1
        self_simis += self_similarity

        other_simlarity = 0.0
        for video2 in filenames:
            if video2 == video1: continue
            start2 = random_start_time()
            other_simlarity += func(video1, start1, video2, start2)
        other_simlarity /= len(filenames) - 1
        other_simis += other_simlarity

        distance += self_similarity - other_simlarity
    distance /= num_iters
    self_simis /= num_iters
    other_simis /= num_iters
    print("The average similarity diff over {} iterations is {:.3f}% ".format(num_iters, distance * 100.0))
    print("The self similarity diff over {} iterations is {:.3f}% ".format(num_iters, self_simis * 100.0))
    print("The other similarity diff over {} iterations is {:.3f}% ".format(num_iters, other_simis * 100.0))
