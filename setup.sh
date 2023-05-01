if [[ -d ./env ]]; then
    echo 'env already exists!'
    exit 0
fi

python -m venv env

echo 'env created!'

if [[ -d ./env/bin ]]; then
    bin_path='./env/bin'
elif [[ -d ./env/Scripts ]]; then
    bin_path='./env/Scripts'
fi

echo 'env files are in:' $bin_path

$bin_path/pip install pypdf