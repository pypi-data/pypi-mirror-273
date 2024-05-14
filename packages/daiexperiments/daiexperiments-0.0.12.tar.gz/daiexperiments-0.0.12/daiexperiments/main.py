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

            # Parameters
            num_genes = 10
            population_size = 50
            mutation_rate = 0.01
            num_generations = 15

            # Initialize population
            population = np.random.randint(0, 10, size=(population_size, num_genes))

            # Define fitness function
            def fitness(chromosome):
                return -np.sum(chromosome)

            # Evolution loop
            for generation in range(num_generations):
                fitness_values = [fitness(chromosome) for chromosome in population]

                # Select individuals for next generation
                selected_indices = np.random.choice(range(population_size), size=population_size, replace=True)
                population = population[selected_indices]

                # Apply mutation
                mutation_mask = np.random.random(size=population.shape) < mutation_rate
                population ^= mutation_mask

                best_fitness = np.max(fitness_values)
                average_fitness = np.mean(fitness_values)
                print(f"Generation {generation+1}, Best Fitness: {best_fitness}, Average Fitness: {average_fitness}")

                best_solution_index = np.argmax(fitness_values)
                best_solution = population[best_solution_index]
                print("Best Solution:", best_solution)

           """
    return code

def face_detection():
    code = """
            # library
            import cv2

            # open the image
            img = cv2.imread('id.jpg')

            # face cascade
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

            # face detection function
            def detect_face(img):
                face_img = img.copy()
                face_rects = face_cascade.detectMultiScale(face_img, scaleFactor=1.3, minNeighbors=3)
                for (x,y,w,h) in face_rects:
                    cv2.rectangle(face_img, (x,y), (x+w,y+h), (0,0,255), 2)
                return face_img

            # apply the face detection function
            face_img = detect_face(img)


            import matplotlib.pyplot as plt
            # display the result
            face_img_np = np.array(face_img)
            plt.imshow(face_img_np)
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

def magic_square():
    code = """
            import random

            def create_magic_square():
            
                nums = list(range(1, 10))
                random.shuffle(nums)
                square = []
                for i in range(0, 9, 3):
                    square.append(nums[i:i+3])

                return square

            def is_magic_square(square):

                target_sum = sum(square[0])  # Sum of the first row

                # Check rows
                for row in square:
                    if sum(row) != target_sum:
                        return False

                # Check columns
                for col in range(3):
                    if sum(row[col] for row in square) != target_sum:
                        return False

                # Check diagonals
                if sum(square[i][i] for i in range(3)) != target_sum:
                    return False
                if sum(square[i][2-i] for i in range(3)) != target_sum:
                    return False

                return True

            def play_game():
            
                print("Welcome to the 3x3 Magic Square Game!")
                square = create_magic_square()
                print("Here's the initial square:")
                for row in square:
                    print(row)

                while True:
                    row1, col1, row2, col2 = map(int, input("Enter the indices of the two numbers you want to swap (row1 col1 row2 col2): ").split())
                    row1 -= 1
                    col1 -= 1
                    row2 -= 1
                    col2 -= 1

                    if (
                        row1 < 0 or row1 > 2 or col1 < 0 or col1 > 2 or
                        row2 < 0 or row2 > 2 or col2 < 0 or col2 > 2
                    ):
                        print("Invalid indices. Try again.")
                        continue

                    square[row1][col1], square[row2][col2] = square[row2][col2], square[row1][col1]

                    print("Updated square:")
                    for row in square:
                        print(row)

                    if is_magic_square(square):
                        print("Congratulations! You have created a magic square!")
                        break

                    print("Keep trying!")

            play_game()
           """
    return code

def genetic_algorithm_meghs():
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
    
def least_square_regression():
    code = """
            # Importing necessary libraries
            import numpy as np
            from sklearn.model_selection import train_test_split
            from sklearn.linear_model import LinearRegression
            from sklearn.metrics import mean_squared_error

            # Generating some sample data
            np.random.seed(0)
            X = 2 * np.random.rand(100, 1)  # Generating 100 random numbers between 0 and 2
            y = 4 + 3 * X + np.random.randn(100, 1)  # Linear equation with some noise

            # Splitting the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Creating a linear regression model
            model = LinearRegression()

            # Fitting the model to the training data
            model.fit(X_train, y_train)

            # Making predictions on the testing data
            y_pred = model.predict(X_test)

            # Calculating the mean squared error
            mse = mean_squared_error(y_test, y_pred)
            print("Mean Squared Error:", mse)
           """
    return code

def k_means_clustering():

    code = '''
            from sklearn.datasets import load_iris
            import pandas as pd
            from sklearn.model_selection import train_test_split
            import matplotlib.pyplot as plt
            from sklearn.cluster import KMeans

            # Load iris dataset
            iris = load_iris()
            df = pd.DataFrame(iris.data, columns=iris.feature_names)
            y = iris.target

            # Concatenate features and labels
            data = pd.concat([df, pd.Series(y, name='label')], axis=1)

            inertias = []
            for i in range(1, 11):
                kmeans = KMeans(n_clusters=i)
                kmeans.fit(data)
                inertias.append(kmeans.inertia_)

            plt.plot(range(1, 11), inertias, marker='o')
            plt.title('Elbow method')
            plt.xlabel('Number of clusters')
            plt.ylabel('Inertia')
            plt.show()
            kmeans = KMeans(n_clusters=3)
            kmeans.fit(data)

            plt.scatter(df.iloc[:, 0], df.iloc[:, 1], c=kmeans.labels_, cmap='viridis')
            centers = kmeans.cluster_centers_
            plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.5) 
            plt.xlabel(iris.feature_names[0])
            plt.ylabel(iris.feature_names[1])
            plt.title('KMeans Clustering')
            plt.show()
           '''
    return code

def binary_classification():
    
    code = """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

cancer=load_breast_cancer()
x=cancer.data
y=cancer.target

print(x,"\n-----------------\n",y)

scaler=StandardScaler()
x=scaler.fit_transform(x)

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)

svm=SVC(kernel='linear')
svm.fit(x_train,y_train)
svm_pred=svm.predict(x_test)

log_reg=LogisticRegression()
log_reg.fit(x_train,y_train)
log_pred=log_reg.predict(x_test)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(x_train, y_train)
knn_pred=knn.predict(x_test)

print("Logistic Regression: \n",classification_report(y_test,log_pred))
print("Support vector machine: \n",classification_report(y_test,svm_pred))
print("K Nearest Neighbors: \n",classification_report(y_test,knn_pred))

models=['Logistic Regression','SVM','KNN']
acc=[accuracy_score(y_test,log_pred),accuracy_score(y_test,svm_pred),accuracy_score(y_test,knn_pred)]
plt.ylim(0.8,1)
plt.bar(models,acc)

import seaborn as sns
print("Logistic Regression")
sns.heatmap(confusion_matrix(y_test, log_pred),annot=True)

print("SVM")
sns.heatmap(confusion_matrix(y_test, svm_pred),annot=True)

print("KNN")
sns.heatmap(confusion_matrix(y_test, knn_pred),annot=True)
           """
    return code

def least_square_regression_hithesh():
    code = """
# Importing Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing

# Loading dataset
california_housing = fetch_california_housing(as_frame=True)
data = california_housing.frame

# Plotting the data
plt.scatter(data['MedInc'], data['AveRooms'])

# Computing X and Y
X = data['MedInc'].values
Y = data['AveRooms'].values

# Mean of variables X and Y
mean_x = np.mean(X)
mean_y = np.mean(Y)

# Total number of data values
n = len(X)

# Calculating 'm' and 'c'
num = 0
denom = 0
for i in range(n):
    num += (X[i] - mean_x) * (Y[i] - mean_y)
    denom += (X[i] - mean_x) ** 2
m = num / denom
c = mean_y - (m * mean_x)

# Printing coefficients
print("Coefficients")
print(m, c)

# Plotting Values and Regression Line
maxx_x = np.max(X) + 1
minn_x = np.min(X) - 1

# line values for x and y
x = np.linspace(minn_x, maxx_x, 1000)
y = c + m * x

# Plotting Regression Line
plt.plot(x, y, label='Regression Line')

# Plotting Scatter Points
plt.scatter(X, Y)

plt.xlabel('Median Income')
plt.ylabel('Average Rooms')
plt.legend()
plt.show()

    """
    return code

def import_statements():
    
    code = """
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler()

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test ...
from sklearn.metrics import accuracy_score, classification_report

svm_pred = svm.predict(x_test)
accuracy_score(y_test,svm_pred)



from sklearn.metrics import confusion_matrix
import seaborn as sns

conf_matrix = confusion_matrix(y_test, svm_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, cmap='Blues', fmt='d', xticklabels=bc.target_names, yticklabels=bc.target_names)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix - SVM')
plt.show()

"""
    return code

def k_means_ishan():

    code = """
    features = df[['math score','reading score','writing score']]
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    import sklearn
    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters = 3, random_state=42)
    kmeans.fit(scaled_features)
    cluster_centers = kmeans.cluster_centers_
    cluster_labels = kmeans.labels_
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    principle_components = pca.fit_transform(scaled_features)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8,6))
    plt.scatter(principle_components[:,0], principle_components[:,1], c = cluster_labels, cmap = 'viridis')
    plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], c='red', marker='x', s=100, label='Cluster Centers')
"""
    return code