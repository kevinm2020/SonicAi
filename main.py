from agent import SonicAgent

def main():
    agent = SonicAgent()

    song = input("Enter a song name: ")
    artist = input("Enter the artist name: ")

    result = agent.analyze(song, artist)

    print("Analysis Result:")
    print(result)

if __name__ == "__main__":
    main()