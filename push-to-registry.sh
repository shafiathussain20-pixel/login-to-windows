#!/bin/bash
# Docker Registry Push Script

# Configuration
REGISTRY="${1:-docker.io}"  # Default to Docker Hub
USERNAME="${2:-your-username}"  # Replace with your Docker Hub username
IMAGE_NAME="login-app"
IMAGE_TAG="latest"

# Construct full image name
FULL_IMAGE_NAME="${USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"

echo "=========================================="
echo "Docker Registry Push Script"
echo "=========================================="
echo "Registry: $REGISTRY"
echo "Image: $FULL_IMAGE_NAME"
echo ""

# Step 1: Login to registry
echo "[1/4] Logging into $REGISTRY..."
docker login -u "$USERNAME" "$REGISTRY"
if [ $? -ne 0 ]; then
    echo "❌ Login failed. Exiting."
    exit 1
fi
echo "✓ Login successful"
echo ""

# Step 2: Build the image
echo "[2/4] Building image: $FULL_IMAGE_NAME..."
docker build -t "$FULL_IMAGE_NAME" .
if [ $? -ne 0 ]; then
    echo "❌ Build failed. Exiting."
    exit 1
fi
echo "✓ Build successful"
echo ""

# Step 3: Run tests (optional)
echo "[3/4] Running unit tests..."
docker run --rm "$FULL_IMAGE_NAME" python -m unittest test_app.py -v
if [ $? -ne 0 ]; then
    echo "⚠ Tests failed, but continuing with push..."
else
    echo "✓ All tests passed"
fi
echo ""

# Step 4: Push to registry
echo "[4/4] Pushing image to $REGISTRY..."
docker push "$FULL_IMAGE_NAME"
if [ $? -ne 0 ]; then
    echo "❌ Push failed. Exiting."
    exit 1
fi
echo "✓ Push successful"
echo ""

echo "=========================================="
echo "✓ Successfully pushed $FULL_IMAGE_NAME"
echo "=========================================="
echo ""
echo "To pull this image later, run:"
echo "  docker pull $FULL_IMAGE_NAME"
echo ""
echo "To run the image, use:"
echo "  docker run -it -v ./users.db:/app/users.db $FULL_IMAGE_NAME"
