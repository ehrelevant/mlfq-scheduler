from view import MLFQView
from controller import MLFQController
from model import MLFQModel

# Initialize MVC Structure and Start the program
def main() -> None:
    model = MLFQModel()
    view = MLFQView()
    
    controller = MLFQController(model, view)
    controller.begin_simulation()

if __name__ == '__main__':
    main()
