"""
Avro file reader to pick out specific alert packet from combined avro file
"""
from fastavro import reader


def pick_alert(
    avro_path: str,
    candid: int,
) -> list:
    """
    Pick out specific alert packet from combined avro file

    Parameters:
    ----------
    avro_path : str
        Path to avro file
    candid: int
        Candidate ID; unique identifier

    Returns:
    ----------
    candidate_record: list
        alert packet
    """
    candidate_record = []
    with open(avro_path, "rb") as avro_f:
        avro_reader = reader(avro_f)
        for record in avro_reader:
            if record["candid"] == candid:
                candidate_record.append(record)

    return candidate_record
