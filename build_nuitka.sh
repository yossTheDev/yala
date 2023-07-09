echo "Building YALA with Nuitka"

echo "Start Poetry Shell"
poetry install
poetry shell

echo "Cleanning..."
rm dist -r

echo "Building..."
python -m nuitka main.py --standalone --onefile --output-filename=yala --output-dir=dist/

echo "Compressing..."
cd dist
tar -cf yala.tar.gz yala --auto-compress 