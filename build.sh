echo "Building YALA"

echo "Start Poetry Shell"
poetry install
poetry shell

echo "Cleanning..."
rm /dist -r

echo "Building..."
pyinstaller app.spec

echo "Compressing..."
cd dist
tar -cf yala.tar.gz yala --auto-compress 