# Simple Chatbot with Rule Based Responses

def get_response(user_input):
    user_input = user_input.lower()
    greetings = ["hello", "hi", "hey", "good morning", "good evening"]
    colours = ["colour", "color"]
    places = ["place", "city", "country"]
    foods = ["food", "dish", "eat"]
    cars = ["car", "vehicle", "automobile"]
    movies = ["movie", "film", "cinema"]
    books = ["book", "novel", "read"]

    if any(greet in user_input for greet in greetings):
        return "Hello! How can I help you today?"
    elif any(word in user_input for word in colours):
        return "My favourite colour is blue."
    elif any(word in user_input for word in places):
        return "I love visiting switzerland, it's a fascinating city!"
    elif any(word in user_input for word in foods):
        return "Pizza is my favourite food."
    elif any(word in user_input for word in cars):
        return "I like electric cars, especially Tesla."
    elif any(word in user_input for word in movies):
        return "My favourite movie is 'Inception'."
    elif any(word in user_input for word in books):
        return "I enjoy reading 'To Kill a Mockingbird'."
    else:
        return "Sorry, I didn't understand that. Can you ask something else?"

def main():
    print("Chatbot: Hi! Ask me about my favourite colour, place, food, car, movie, or book.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye!")
            break
        response = get_response(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()
