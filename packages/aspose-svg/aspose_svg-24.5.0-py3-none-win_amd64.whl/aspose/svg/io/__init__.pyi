from typing import List, Optional, Dict, Iterable
import aspose.pycore
import aspose.pydrawing
import aspose.svg
import aspose.svg.builder
import aspose.svg.collections
import aspose.svg.converters
import aspose.svg.datatypes
import aspose.svg.diagnostics
import aspose.svg.dom
import aspose.svg.dom.attributes
import aspose.svg.dom.canvas
import aspose.svg.dom.css
import aspose.svg.dom.events
import aspose.svg.dom.mutations
import aspose.svg.dom.traversal
import aspose.svg.dom.traversal.filters
import aspose.svg.dom.views
import aspose.svg.dom.xpath
import aspose.svg.drawing
import aspose.svg.drawing.skiasharp
import aspose.svg.events
import aspose.svg.filters
import aspose.svg.imagevectorization
import aspose.svg.io
import aspose.svg.net
import aspose.svg.net.headers
import aspose.svg.net.messagefilters
import aspose.svg.net.messagehandlers
import aspose.svg.paths
import aspose.svg.rendering
import aspose.svg.rendering.devices
import aspose.svg.rendering.fonts
import aspose.svg.rendering.image
import aspose.svg.rendering.pdf
import aspose.svg.rendering.pdf.encryption
import aspose.svg.rendering.styles
import aspose.svg.rendering.styles.paintservers
import aspose.svg.rendering.xps
import aspose.svg.saving
import aspose.svg.saving.resourcehandlers
import aspose.svg.services
import aspose.svg.toolkit
import aspose.svg.toolkit.optimizers
import aspose.svg.window

class FileCreateStreamProvider(ICreateStreamProvider):
    '''Represents :py:class:`System.IO.FileStream` implementation for providing streams to the rendering devices.'''
    
    @overload
    def get_stream(self, name : str, extension : str) -> io.RawIOBase:
        '''Provides a stream for rendering.
        
        :param name: The name of the stream.
        :param extension: The file name extension to use if a file stream is being created.
        :returns: A Stream object that is used for writing data during the rendering operations.'''
        ...
    
    @overload
    def get_stream(self, name : str, extension : str, page : int) -> io.RawIOBase:
        '''Provides a stream for rendering.
        
        :param name: The name of the stream.
        :param extension: The file name extension to use if a file stream is being created.
        :param page: The page number of the document.
        :returns: A Stream object that is used for writing data during the rendering operations.'''
        ...
    
    def release_stream(self, stream : io.RawIOBase):
        '''Releases the stream.
        
        :param stream: The stream being released.'''
        ...
    
    @property
    def directory(self) -> str:
        '''Gets the directory.'''
        ...
    
    @directory.setter
    def directory(self, value : str):
        '''Sets the directory.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the name.'''
        ...
    
    ...

class IBlob:
    '''A Blob object refers to a byte sequence, and has a size attribute which is the total number of bytes in the byte sequence, and a type attribute, which is an ASCII-encoded string in lower case representing the media type of the byte sequence.'''
    
    def slice(self, start : int, end : int, content_type : str) -> aspose.svg.io.IBlob:
        '''Returns a new Blob object with bytes ranging from the optional start parameter up to but not including the optional end parameter,
        and with a type attribute that is the value of the optional contentType parameter.
        
        :param start: The parameter is a value for the start point of a slice
        :param end: The parameter is a value for the start point of a slice
        :param content_type: The parameter is a media type of the Blob
        :returns: Returns a new Blob object with bytes ranging from the optional start parameter up to but not including the optional end parameter, and with a type attribute that is the value of the optional contentType parameter.'''
        ...
    
    @property
    def size(self) -> int:
        '''Returns the size of the byte sequence in number of bytes.
        On getting, conforming user agents must return the total number of bytes that can be read by a FileReader
        or FileReaderSync object, or 0 if the Blob has no bytes to be read.'''
        ...
    
    @property
    def type(self) -> str:
        '''The ASCII-encoded string in lower case representing the media type of the Blob.
        On getting, user agents must return the type of a Blob as an ASCII-encoded string in lower case,
        such that when it is converted to a byte sequence, it is a parsable MIME type,
        or the empty string – 0 bytes – if the type cannot be determined.'''
        ...
    
    ...

class ICreateStreamProvider:
    '''Represents an interface that can be implemented by classes providing streams to the rendering devices.'''
    
    @overload
    def get_stream(self, name : str, extension : str) -> io.RawIOBase:
        '''Provides a stream for rendering.
        
        :param name: The name of the stream.
        :param extension: The file name extension to use if a file stream is being created.
        :returns: A Stream object that is used for writing data during the rendering operations.'''
        ...
    
    @overload
    def get_stream(self, name : str, extension : str, page : int) -> io.RawIOBase:
        '''Provides a stream for rendering.
        
        :param name: The name of the stream.
        :param extension: The file name extension to use if a file stream is being created.
        :param page: The page number of the document.
        :returns: A Stream object that is used for writing data during the rendering operations.'''
        ...
    
    def release_stream(self, stream : io.RawIOBase):
        '''Releases the stream.
        
        :param stream: The stream being released.'''
        ...
    
    ...

class IFile(IBlob):
    '''A File object is a Blob object with a name attribute, which is a string; it can be created within the web application via a constructor, or is a reference to a byte sequence from a file from the underlying (OS) file system.'''
    
    def slice(self, start : int, end : int, content_type : str) -> aspose.svg.io.IBlob:
        '''Returns a new Blob object with bytes ranging from the optional start parameter up to but not including the optional end parameter,
        and with a type attribute that is the value of the optional contentType parameter.
        
        :param start: The parameter is a value for the start point of a slice
        :param end: The parameter is a value for the start point of a slice
        :param content_type: The parameter is a media type of the Blob
        :returns: Returns a new Blob object with bytes ranging from the optional start parameter up to but not including the optional end parameter, and with a type attribute that is the value of the optional contentType parameter.'''
        ...
    
    @property
    def name(self) -> str:
        '''The name of the file.
        On getting, this must return the name of the file as a string.'''
        ...
    
    @property
    def last_modified(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Returns the size of the byte sequence in number of bytes.
        On getting, conforming user agents must return the total number of bytes that can be read by a FileReader
        or FileReaderSync object, or 0 if the Blob has no bytes to be read.'''
        ...
    
    @property
    def type(self) -> str:
        '''The ASCII-encoded string in lower case representing the media type of the Blob.
        On getting, user agents must return the type of a Blob as an ASCII-encoded string in lower case,
        such that when it is converted to a byte sequence, it is a parsable MIME type,
        or the empty string – 0 bytes – if the type cannot be determined.'''
        ...
    
    ...

class IFileList:
    '''Represent the interface for list of files.'''
    
    @property
    def length(self) -> int:
        '''Return length for list of files.'''
        ...
    
    def __getitem__(self, key : int) -> aspose.svg.io.IFile:
        '''Returns the indexth file in the list.'''
        ...
    
    ...

class IOutputStorage:
    '''Provides the creation and management of output streams :py:class:`aspose.svg.io.OutputStream`.'''
    
    def create_stream(self, context : aspose.svg.io.OutputStreamContext) -> aspose.svg.io.OutputStream:
        '''Creates the output stream :py:class:`aspose.svg.io.OutputStream`.
        
        :param context: Specifies the output stream context :py:class:`aspose.svg.io.OutputStreamContext`.
        :returns: The output stream.'''
        ...
    
    def release_stream(self, stream : aspose.svg.io.OutputStream):
        '''Releases the output stream.
        
        :param stream: The output stream.'''
        ...
    
    ...

class LocalFileSystemStorage(IOutputStorage):
    '''A file system storage.'''
    
    def create_stream(self, context : aspose.svg.io.OutputStreamContext) -> aspose.svg.io.OutputStream:
        '''Creates the output file stream :py:class:`aspose.svg.io.OutputStream`.
        
        :param context: Specifies the output stream context :py:class:`aspose.svg.io.OutputStreamContext`.
        :returns: The output file stream.'''
        ...
    
    def release_stream(self, stream : aspose.svg.io.OutputStream):
        '''Releases the output file stream.
        
        :param stream: The output file stream.'''
        ...
    
    @property
    def output_directory(self) -> str:
        ...
    
    @output_directory.setter
    def output_directory(self, value : str):
        ...
    
    ...

class OutputStream:
    '''A surrogate stream wraps the real output stream and controls access to it.
    :py:class:`aspose.svg.io.OutputStream` contains URI data that describes location of the output stream.'''
    
    @property
    def uri(self) -> str:
        '''Gets the URI of stream location.'''
        ...
    
    ...

class OutputStreamContext:
    '''A context for initialization of the output stream.'''
    
    @property
    def uri(self) -> str:
        '''Gets the original URI of the saved resource.'''
        ...
    
    ...

