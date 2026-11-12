"""核对事件流前导长度和冻结列名。"""
import struct
from .io import asset,integer

def summarize(v,root):
    raw,digest=asset(root,v['source']);integer(v['chunk_size'],1)
    if len(raw)<12:raise ValueError('事件流前导不完整')
    if not v['columns'] or len(set(v['columns']))!=len(v['columns']):raise ValueError('列名为空或重复')
    return {'raw_bytes':len(raw),'sha256':digest,'first_message_declared_bytes':struct.unpack('>I',raw[:4])[0],'columns':v['columns']}
