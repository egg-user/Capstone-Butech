const multer = require('multer')
const path = require('path')

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'images');
    },
    filename: (req, file, cb) => {
        const timestamp = new Date().getTime();
        const originalname = file.originalname;
        // const extension = path.extname(file.originalname);

        cb(null, `${timestamp}-${originalname}`);
    }
});

const upload = multer({storage: storage})

module.exports = upload