import os,time,random,hashlib,shutil
from flask import jsonify
from werkzeug.utils import secure_filename
from abstract_pandas import get_df,safe_excel_save
from werkzeug.datastructures import FileStorage
import os
class fileManager:
    _instance = None

    def __init__(self, allowed_extentions=None):
        if fileManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            fileManager._instance = self

        # Base path is the directory of the script if not specified
        self.allowed_extentions = allowed_extentions or {'ods','csv','xls','xlsx','xlsb'}

    @staticmethod
    def get_instance(allowed_extentions=None):
        if fileManager._instance is None:
            fileManager(allowed_extentions)
        return fileManager._instance

        
class AbsManager:
    _instance = None

    def __init__(self, base_path=None):
        if AbsManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            AbsManager._instance = self

        # Base path is the directory of the script if not specified
        self.base_path = base_path or os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def get_instance(base_path=None):
        if AbsManager._instance is None:
            AbsManager(base_path)
        return AbsManager._instance

    def _make_dir(self, path):
        """ Create directory if it doesn't exist. """
        os.makedirs(path, exist_ok=True)
        return path

    # Basic directories
    def get_base_path(self):
        return self.base_path
    
    def get_converts_dir(self):
        return self._make_dir(os.path.join(self.get_base_path(), 'converts'))
    
    def get_users_dir(self):
        return self._make_dir(os.path.join(self.get_base_path(), 'users'))

    def get_uploads_dir(self):
        return self._make_dir(os.path.join(self.get_base_path(), 'uploads'))

    def get_downloads_dir(self):
        return self._make_dir(os.path.join(self.get_base_path(), 'downloads'))

    # User-specific directories
    def get_user_dir(self, user):
        return self._make_dir(os.path.join(self.get_users_dir(), user))
    
    def get_user_converts_dir(self, user):
        return self._make_dir(os.path.join(self.get_user_dir(user), 'converts'))

    def get_user_uploads_dir(self, user):
        return self._make_dir(os.path.join(self.get_user_dir(user), 'uploads'))

    def get_user_downloads_dir(self, user):
        return self._make_dir(os.path.join(self.get_user_dir(user), 'downloads'))

    def get_user_process_dir(self, user):
        return self._make_dir(os.path.join(self.get_user_dir(user), 'process'))

    def get_user_saved_dir(self, user):
        return self._make_dir(os.path.join(self.get_user_dir(user), 'saved'))

    # File path generation (without creating directories)
    def get_file_path(self, directory, fileName):
        return os.path.join(directory, fileName)
def get_user_downloads_file_path(user,fileName):
    abs_manager = AbsManager.get_instance()
    user_downloads_dir = abs_manager.get_user_downloads_dir(user)
    return abs_manager.get_file_path(user_downloads_dir, fileName)
def get_user_process_file_path(user,fileName):
    abs_manager = AbsManager.get_instance()
    user_process_dir = abs_manager.get_user_process_dir(user)
    return abs_manager.get_file_path(user_process_dir, fileName)
def get_user_uploads_file_path(user,fileName):
    abs_manager = AbsManager.get_instance()
    user_uploads_dir = abs_manager.get_user_uploads_dir(user)
    return abs_manager.get_file_path(user_uploads_dir, fileName)
def get_user_saved_file_path(user,fileName):
    abs_manager = AbsManager.get_instance()
    user_saved_dir = abs_manager.get_user_saved_dir(user)
    return abs_manager.get_file_path(user_saved_dir, fileName)
def get_user_converts_file_path(user,fileName):
    abs_manager = AbsManager.get_instance()
    user_converts_dir = abs_manager.get_user_converts_dir(user)
    return abs_manager.get_file_path(user_converts_dir, fileName)
def copy_to(path_1,path_2):
    if os.path.isfile(path_1):
        shutil.copy(path_1,path_2)
        print(f"copyd from {path_1}\n to {path_2}\n\n")
        return path_2
    print(f"not copyd from {path_1}\n to {path_2}\n\n")
    return False
def manual_move(path_1,path_2):
    try:
        if os.path.isfile(path_1):
            save_file(file=read_file(path_1),file_path=path_2)
        cleanup_files(path_1)
    except Exception as e:
       print(f"{e}")
       return False
    return path_2
def move_to(path_1,path_2):
    if os.path.isfile(path_1):
        try:
            shutil.move(path_1,path_2)
        except:
            return manual_move(path_1,path_2)
        print(f"moved from {path_1} to {path_2}\n\n")
        return path_2
    print(f"not moved from {path_1} to {path_2}\n\n")
    return False
def move_from_process(user,fileName):
    process_file_path = get_user_process_file_path(user,fileName)
    downloads_file_path = get_user_downloads_file_path(user,fileName)
    return move_to(process_file_path,downloads_file_path)
def move_to_process(user,fileName):
    uploads_file_path = get_user_uploads_file_path(user,fileName)
    process_file_path = get_user_process_file_path(user,fileName)
    return move_to(uploads_file_path,process_file_path)
def copy_to_saved(user,fileName):
    downloads_file_path = get_user_downloads_file_path(user,fileName)
    saved_file_path = get_user_saved_file_path(user,fileName)
    return copy_to(downloads_file_path,saved_file_path)
def convert_file(file_path,converts_file_path):
    original_dirName = get_dirname(file_path)
    conv_file_name = get_file_name(converts_file_path)
    new_file_path = os.path.join(original_dirName,conv_file_name)
    moved = move_to(converts_file_path,new_file_path)
    if moved:
        cleanup_files(file_path)
        return moved
    return False
def is_storage(obj):
    if isinstance(obj, FileStorage):  # Check if source is a FileStorage object
        return True
    return False
def get_file_name(obj):
    if is_storage(obj):
        try:
            # Read the file directly from the file object
            file_name = secure_filename(obj.filename)
            return file_name
        except Exception as e:
            print(f"Failed to read file: {e}")
    if isinstance(obj,str) and (os.path.isfile(obj) or os.path.isdir(os.path.dirname(obj))):
         return os.path.basename(obj)
    return obj
def generate_custom_uid():
    """
    Generates a custom unique identifier using a combination of the current time (to the millisecond)
    and a random number, hashed for uniformity and to obscure the raw data.
    """
    timestamp = int(time.time() * 1000)  # Current time in milliseconds
    random_int = random.randint(0, 999999)  # Random integer
    raw_uid = f"{timestamp}-{random_int}"
    hash_uid = hashlib.sha256(raw_uid.encode()).hexdigest()  # Creating a SHA-256 hash of the ID
    return hash_uid[:16]  # Return the first 16 characters for a shorter UID
def insert_into_tail(file_path,string):
    dirName = os.path.dirname(file_path)
    baseName = os.path.basename(file_path)
    fileName,ext=os.path.splitext(baseName)
    newName = f"{fileName}_{string}{ext}"
    if dirName:
        newName = os.path.join(dirName,baseName)
    return newName
def get_unique_file_name(obj):
    dirname = get_dirname(obj)
    fileName= insert_into_tail(get_file_name(obj),generate_custom_uid())
    if dirname:
        return os.path.join(dirname,fileName)
    return fileName
def validate_user_and_filename(user, filename):
    """Validate presence of user and filename."""
    if not user or not filename:
        return jsonify({'error': True, 'message': "User or filename not specified"}), 400
    return None

def file_exists(file_path):
    """Check if a file exists at the specified path and return appropriate responses."""
    if not os.path.isfile(file_path):
        if os.path.isdir(os.path.dirname(file_path)):
            message = f'File {os.path.basename(file_path)} does not exist'
        else:
            message = 'User directory does not exist'
        return jsonify({'error': True, "message": message}), 400
    return None

def cleanup_files(*paths):
    """Remove files from the filesystem as a cleanup process."""
    for path in paths:
        if os.path.isfile(path):
            os.remove(path)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in fileManager.get_instance().allowed_extentions

def read_file(file=None,file_path=None):
    if file and is_storage(file):
        return file.read()
    elif file_path and os.path.splitext(file_path)[-1][1:] in ['ods','csv','xls','xlsx','xlsb']:
         return get_df(file_path)
    else:
        return safe_read_from_json(file_path)


def save_file(file=None,file_path=None):
    if file and is_storage(file):
        file.save(file_path)
    elif file_path and os.path.splitext(file_path)[-1][1:] in ['ods','csv','xls','xlsx','xlsb']:
         safe_excel_save(get_df(file_path),file_path)
    else:
        write_to_file(contents=file,file_path=file_path)
def get_dirname(obj):
    if isinstance(obj,str) and (os.path.isfile(obj) or os.path.isdir(os.path.dirname(obj))):
        return os.path.dirname(obj)
def get_file_name(obj):
    if is_storage(obj):
        try:
            # Read the file directly from the file object
            filename = secure_filename(obj.filename)
            return filename
        except Exception as e:
            print(f"Failed to read file: {e}")
    if isinstance(obj,str) and (os.path.isfile(obj) or os.path.isdir(os.path.dirname(obj))):
         return os.path.basename(obj)
    return obj

def upload_file(file,user=None):
    if file is None:
        return jsonify({'error': True, 'message': "No file uploaded"}), 400
    filename = get_file_name(file)
    if not allowed_file(filename):
        return jsonify({'error': True, 'message': "File type not allowed"}), 400
    
    if user == None:
        user='Defaut'
    unique_name = get_unique_file_name(filename)
    upload_file_path = get_user_uploads_file_path(user,unique_name)
    save_file(file,upload_file_path)
    return {'success': True, 'fileName': unique_name,"user":user}

def download_user_file(user=None,fileName=None):
    upload_file_path = get_user_uploads_file_path(user, fileName)
    download_file_path = get_user_downloads_file_path(user, fileName)
    processed_file_path = get_user_process_file_path(user, fileName)
    upload_file_veri = os.path.isfile(upload_file_path)
    processed_file_veri = os.path.isfile(processed_file_path)
    download_file_veri = os.path.isfile(download_file_path)
    if upload_file_veri and processed_file_veri:
        return jsonify({'error': True, "message": "still processing"}), 400
    if not upload_file_veri and processed_file_veri:
        return jsonify({'error': True, "message": "possibly still processing"}), 400
    if upload_file_veri and not processed_file_veri and not download_file_veri or not upload_file_veri and not processed_file_veri and not download_file_veri:
        return jsonify({'error': True, "message": "file will not exist"}), 500
