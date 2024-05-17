import os
import pkg_resources

def get_form(filled_out=False, output_path=None):
    """ Download the standardized PDF form.

    Args:
        filled_out (bool, optional): If True, download the filled-out version of the form. Default is False (blank form).
        output_path (str, optional): The path where the PDF file should be saved. If not provided, the file will be saved in the current working directory.

    Returns:
        str: The path to the downloaded PDF file.
    """
    if filled_out:
        form_file = 'standard-form-filled-out.pdf'
    else:
        form_file = 'standard-form.pdf'

    pdf_file = pkg_resources.resource_filename('feather_extract', os.path.join('data', form_file))

    if output_path is None:
        output_path = os.path.join(os.getcwd(), form_file)
    else:
        output_path = os.path.join(output_path, form_file)

    with open(pdf_file, 'rb') as src, open(output_path, 'wb') as dst:
        dst.write(src.read())

    return output_path