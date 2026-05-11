import logging
import os
import re
import sys

log_file = os.path.join(os.getcwd(), 'HexFindReplace.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def string_to_little_endian_hex(value):
    """Converts a value to its little-endian hexadecimal representation.
    
    If value is numeric (int or float string), converts as little-endian .
    Otherwise, converts the string itself to UTF-8 hex.
    """
    try:
        # Try to convert to number first
        try:
            num_val = float(value)
            int_val = int(num_val)
            
            # Determine how many bytes needed
            if int_val == 0:
                return "00"
            
            # Find minimum bytes needed
            byte_length = (int_val.bit_length() + 7) // 8
            if byte_length == 0:
                byte_length = 1
            
            # Convert to little-endian hex
            hex_str = int_val.to_bytes(byte_length, 'little').hex().upper()
            
            # Add spaces between byte pairs for readability
            return ' '.join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))
        except (ValueError, OverflowError):
            # Not numeric, convert as UTF-8 string
            if isinstance(value, str):
                value_bytes = value.encode('utf-8')
            else:
                value_bytes = bytes(value)
            hex_str = value_bytes.hex().upper()
            return ' '.join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))
    except Exception as e:
        logger.error(f"Error converting to hex: {value} - {e}")
        return None
    
def hex_find_replace(file_path, search_pattern, replace_pattern, occurrence=None):
    """
    Replace hex patterns in a file.
    
    Args:
        file_path: Path to the file to modify
        search_pattern: Hex pattern to search for (?? for wildcards)
        replace_pattern: Hex pattern to replace with
        occurrence: Optional - replace only the X occurrence. If None, replace all.
    """
    # rb = binary
    with open(file_path, "rb") as f:
        data = f.read()

    # Convert hex pattern with ?? wildcards into a regex pattern
    hex_parts = search_pattern.split()
    regex_pattern = b"".join(
        b"." if part == "??" else bytes.fromhex(part) for part in hex_parts
    )

    # string >> bytes
    regex = re.compile(regex_pattern, re.DOTALL)

    # Passed pattern to bytes, wont have ??
    replace_bytes = bytes.fromhex(replace_pattern.replace(" ", ""))

    # Find matches in the file given
    matches = [m.start() for m in regex.finditer(data)]

    if not matches:
        logger.warning("Replace Pattern not found on file.")
        return

    if occurrence is not None:
        if occurrence < 1 or occurrence > len(matches):
            logger.error(f"Occurrence {occurrence} is out of range (1-{len(matches)})")
            return
        matches_to_replace = [matches[occurrence - 1]] #only the X occurrence
        logger.info(f"Found {len(matches)} occurrences, replacing {occurrence}th...")
    else:
        matches_to_replace = matches #all
        logger.info(f"Found {len(matches)} occurrences, replacing all...")

    # Replace occurrences (in reverse order to maintain correct positions)
    new_data = bytearray(data)
    for match in reversed(matches_to_replace):
        # Match is start index of hex search, match + len(replace_bytes) the end of the replacement
        #00 11 22 33 44 55 66 77, replace of 33 44 with 00 00
        #match = 3, match + len(replace_bytes) = 5. 3:5 slice
        new_data[match:match + len(replace_bytes)] = replace_bytes

    # Save
    with open(file_path, "wb") as f:
        f.write(new_data)

    logger.info("Replacement complete!")

def prepare_replace_pattern(replace_pattern):
    """
    Prepares the replace pattern by converting integers within double quotes to
    little-endian hex.  Handles errors more explicitly.
    """
    parts = replace_pattern.split()
    new_parts = []
    for part in parts:
        if part.startswith('"') and part.endswith('"'):
            # Extract the value between the quotes
            value_str = part[1:-1]

            # Attempt conversion to little-endian hex
            hex_value = string_to_little_endian_hex(value_str)

            if hex_value is None:
                return None
            else:
                new_parts.append(hex_value)
        else:
            new_parts.append(part)  # Keep the original part

    return " ".join(new_parts)

if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        logger.error("Usage: python hex_replace.py <file path> <search pattern> <replace pattern> <occurrence>")
        logger.error("occurrence is the only optional parameter.\nEmpty = all matches will be replaced.\nAny value = only replace that value occurrence.")
        sys.exit(1)

    file_path = sys.argv[1]
    search_pattern = sys.argv[2]
    replace_pattern = sys.argv[3]
    occurrence = None

    #checks
    if len(sys.argv) == 5:
        try:
            occurrence = int(sys.argv[4])
        except ValueError:
            logger.error(f"Invalid occurrence number: {sys.argv[4]} (must be an integer)")
            sys.exit(1)
            
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        sys.exit(1)
        
        
    prepared_replace_pattern = prepare_replace_pattern(replace_pattern)
    if prepared_replace_pattern is None:
        logger.error("Failed to prepare replace pattern")
        sys.exit(1)
    
    logger.info(f"File: {file_path}")
    logger.info(f"Search Pattern: {search_pattern}")
    logger.info(f"Replace pattern: {replace_pattern} to {prepared_replace_pattern}")
    logger.info(f"Occurrence: {'All' if occurrence is None else occurrence}")
    try:
        hex_find_replace(file_path, search_pattern, prepared_replace_pattern, occurrence)
    except ValueError as e:
        logger.error(f"ValueError in hex_find_replace: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)