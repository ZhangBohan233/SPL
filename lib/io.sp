/*
 * An input stream that reads text file.
 */
class TextInputStream extends InputStream {

    var fp = null;

    function TextInputStream(file_name) {
        fp = f_open(file_name, "r");
    }

    @Override
    function read() {
        return fp.read();
    }

    function readline() {
        return fp.readline();
    }

    @Override
    function close() {
        return fp.close();
    }
}


/*
 * An input stream that reads binary file.
 */
class FileInputStream extends InputStream {

    var fp = null;

    function FileInputStream(file_name) {
        fp = f_open(file_name, "rb");
    }

    @Override
    function read() {
        return fp.read();
    }

    function read_one() {
        return fp.read_one();
    }

    @Override
    function close() {
        return fp.close();
    }
}


/*
 * An output stream that writes text file.
 */
class TextOutputStream extends OutputStream {

    var fp = null;

    function TextOutputStream(file_name) {
        fp = f_open(file_name, "w");
    }

    @Override
    function write(s) {
        return fp.write(s);
    }

    @Override
    function flush() {
        return fp.flush();
    }

    @Override
    function close() {
        return fp.close();
    }
}


/*
 * An output stream that writes binary file.
 */
class FileOutputStream extends OutputStream {

    var fp = null;

    function FileOutputStream(file_name) {
        fp = f_open(file_name, "wb");
    }

    @Override
    function write(s) {
        return fp.write(s);
    }

    @Override
    function flush() {
        return fp.flush();
    }

    @Override
    function close() {
        return fp.close();
    }
}
