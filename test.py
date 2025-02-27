import cv2

# Simple test to check if cv2.imshow() works
image = cv2.imread('Results/teste.jpg')  # Replace with a path to a valid image
if image is not None:
    cv2.imshow('Test Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Image not found or could not be read")
