    # download pytorch doc.
    export EFS_DIR="./datasets/pytorch"
    
    wget -e robots=off --recursive --no-clobber --page-requisites \
    --html-extension --convert-links --restrict-file-names=windows \
    --domains pytorch.org --no-parent --accept=html --retry-on-http-error=429 \
    -P $EFS_DIR https://pytorch.org/docs/stable