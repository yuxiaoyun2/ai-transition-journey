def square(n):
    try:
        return int(n) ** 2
    except ValueError:
        return None


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <number>")
        return 
    
    result = square(sys.argv[1])
    
    if result is None:
        print("input integer")
    else:
        print(result)
        
if __name__ == "__main__":
    main()