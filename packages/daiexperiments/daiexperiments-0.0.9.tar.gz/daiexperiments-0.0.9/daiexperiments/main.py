def number_plate_detection():
    code = """
            !pip install easyocr
            !pip install imutils

            import cv2
            import matplotlib.pyplot as plt
            import numpy as np
            import easyocr
            import imutils

            image = cv2.imread("C:/Users/mahna/Downloads/car.png")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            plt.imshow(cv2.cvtColor(gray,cv2.COLOR_BGR2RGB))

            bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #noise reduction
            edged = cv2.Canny(bfilter, 30, 200)  # edge detection
            plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))

            keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(keypoints)
            contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

            location = None
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 10, True)
                counter = 0
                if len(approx) == 4:
                        location = approx
                        counter = counter+1
                        if(counter == 3):
                            print(location)
                            break
            
            location

            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(mask, [location], 0, 255, -1)
            new_image = cv2.bitwise_and(image, image, mask = mask)

            plt.imshow(new_image)

            (x,y) = np.where(mask==255)
            (x1,y1) = (np.min(x), np.min(y))
            (x2,y2) = (np.max(x), np.max(y))
            cropped_image = gray[x1:x2+1, y1:y2+1]

            plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

            reader = easyocr.Reader(['en'])
            result = reader.readtext(cropped_image)
            result

            result[0][1]
            """
    return code
    
def genetic_algorithm():
    code = """
            import numpy as np
            num_genes = 10
            population_size = 50
            mutation_rate = 0.01
            num_generations = 15
            population = np.random.randint(0, 10, size=(population_size, num_genes))
            print(population[:10])

            def soft_tissue_characterization(chromosome):
                return np.sum(chromosome)
            def fitness_function(chromosome):
                return -soft_tissue_characterization(chromosome)
            
            for generation in range(num_generations):
                fitness_values = np.apply_along_axis(fitness_function, 1, population)


                selected_indices = []
                for _ in range(population_size):
                    tournament_indices = np.random.choice(range(population_size), size=3, replace=False)
                    tournament_fitness = fitness_values[tournament_indices]
                    winner_index = tournament_indices[np.argmax(tournament_fitness)]
                    selected_indices.append(winner_index)
                selected_population = population[selected_indices]


                crossover_points = np.random.randint(1, num_genes, size=population_size // 2)
                offspring = np.empty_like(population)
                for i in range(0, population_size, 2):
                    parent1, parent2 = selected_population[i], selected_population[i + 1]
                    crossover_point = crossover_points[i // 2]
                    offspring[i, :] = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
                    offspring[i + 1, :] = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))


                mutation_mask = np.random.random(size=offspring.shape) < mutation_rate
                offspring ^= mutation_mask

                population = offspring

                best_fitness = np.max(fitness_values)
                average_fitness = np.mean(fitness_values)
                print(f"Generation {generation+1}, Best Fitness: {best_fitness}, Average Fitness: {average_fitness}")

                best_solution_index = np.argmax(fitness_values)
                best_solution = population[best_solution_index]
                best_soft_tissue_characterization = soft_tissue_characterization(best_solution)
                print("Best Solution:", best_solution)
                print("Best Soft Tissue Characterization:", best_soft_tissue_characterization)
           """
    return code

def face_detection():
    code = """
            pip install opencv-python
            import cv2
            import numpy as np
            import warnings
            warnings.filterwarnings("ignore")
            import matplotlib.pyplot as plt
            import numpy as np
            face_haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            cap = cv2.VideoCapture(0)

            while True:
                ret, test_img = cap.read()  # captures frame and returns boolean value and captured image
                if not ret:
                    continue
                gray_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

                faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)

                for (x, y, w, h) in faces_detected:
                    cv2.rectangle(test_img, (x, y), (x + w, y + h), (255, 0, 0), thickness=7)
                    roi_gray = gray_img[y:y + w, x:x + h]  # cropping region of interest i.e. face area from  image
                    roi_gray = cv2.resize(roi_gray, (224, 224))
                    cv2.putText(test_img, "Face Detected " , (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                resized_img = cv2.resize(test_img, (1000, 700))
                cv2.imshow('Facial emotion analysis ', resized_img)

                if cv2.waitKey(10) == ord('q'):  # wait until 'q' key is pressed
                    break

            cap.release()
            cv2.destroyAllWindows
            """
    return code

def three_cross_three_grid():
    code = """
            import numpy as np

            # Define grid environment
            grid_width = 3
            grid_height = 3
            start_state = (0, 0)
            goal_state = (1, 2)
            obstacles = [(1, 1)]
            actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            num_actions = len(actions)
            num_states = grid_width * grid_height

            # Initialize Q-table
            Q = np.zeros((num_states, num_actions))

            # Define parameters
            alpha = 0.1  # Learning rate
            gamma = 0.9  # Discount factor
            epsilon = 0.1  # Exploration-exploitation trade-off

            # Define helper functions
            def get_state_index(state):
                return state[0] * grid_width + state[1]

            def choose_action(state):
                if np.random.uniform(0, 1) < epsilon:
                    return np.random.choice(actions)
                else:
                    return actions[np.argmax(Q[get_state_index(state), :])]

            def update_Q(state, action, reward, next_state):
                Q[get_state_index(state), actions.index(action)] += alpha * (
                    reward + gamma * np.max(Q[get_state_index(next_state), :]) - Q[get_state_index(state), actions.index(action)]
                )

            # Training
            num_episodes = 1000
            for _ in range(num_episodes):
                state = start_state
                while state != goal_state:
                    action = choose_action(state)
                    next_state = state

                    if action == 'UP' and state[0] > 0:
                        next_state = (state[0] - 1, state[1])
                    elif action == 'DOWN' and state[0] < grid_height - 1:
                        next_state = (state[0] + 1, state[1])
                    elif action == 'LEFT' and state[1] > 0:
                        next_state = (state[0], state[1] - 1)
                    elif action == 'RIGHT' and state[1] < grid_width - 1:
                        next_state = (state[0], state[1] + 1)

                    if next_state in obstacles:
                        reward = -10
                        next_state = state
                    elif next_state == goal_state:
                        reward = 10
                    else:
                        reward = -1

                    update_Q(state, action, reward, next_state)
                    state = next_state

            # Print the Q-table
            print("Q-table:")
            for i in range(num_states):
                print(f"State {i}: {Q[i]}")

            # Testing
            state = start_state
            while state != goal_state:
                action = actions[np.argmax(Q[get_state_index(state), :])]
                print(f"Current State: {state}, Action: {action}")
                if action == 'UP' and state[0] > 0:
                    state = (state[0] - 1, state[1])
                elif action == 'DOWN' and state[0] < grid_height - 1:
                    state = (state[0] + 1, state[1])
                elif action == 'LEFT' and state[1] > 0:
                    state = (state[0], state[1] - 1)
                elif action == 'RIGHT' and state[1] < grid_width - 1:
                    state = (state[0], state[1] + 1)
           """
    return code

def three_cross_three_grid_rl():
    code = """
            import gym
            import numpy as np

            # Create FrozenLake environment
            env = gym.make("FrozenLake-v1")

            # Initialize Q-table
            num_states = env.observation_space.n
            num_actions = env.action_space.n
            Q = np.zeros((num_states, num_actions))

            # Q-learning parameters
            alpha = 0.8  # Learning rate
            gamma = 0.95  # Discount factor
            epsilon = 0.1  # Exploration rate

            # Q-learning algorithm
            num_episodes = 10000
            for episode in range(num_episodes):
                state = env.reset()
                done = False
                while not done:
                    # Choose action
                    if np.random.uniform(0, 1) < epsilon:
                        action = env.action_space.sample()  # Explore
                    else:
                        action = np.argmax(Q[state])  # Exploit

                    # Take action
                    next_state, reward, done, _ = env.step(action)

                    # Update Q-table
                    Q[state, action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])

                    state = next_state

            # Print the Q-table
            print("Q-table:")
            print(Q)

            # Test the trained agent
            num_test_episodes = 10
            total_rewards = 0
            for _ in range(num_test_episodes):
                state = env.reset()
                done = False
                while not done:
                    action = np.argmax(Q[state])
                    next_state, reward, done, _ = env.step(action)
                    total_rewards += reward
                    state = next_state

            avg_reward = total_rewards / num_test_episodes
            print(f"Average reward over {num_test_episodes} test episodes: {avg_reward}")
           """
    return code