import io
from typing import Union
from PyPDF2 import PdfReader
from fastapi.responses import FileResponse
import pandas as pd
from fastapi import FastAPI, File, UploadFile
from typing import Annotated
from fastapi.responses import StreamingResponse

app = FastAPI()


@app.post('/api/get_true_sign_from_pdf/')
async def get_true_sign_from_pdf(file: UploadFile):
    return StreamingResponse(io.BytesIO(convert_to_excel(file)), media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #return FileResponse(path=convert_to_excel(file), filename='Статистика покупок.xlsx', media_type='multipart/form-data')

def convert_to_excel(file):
    reader = PdfReader(file.file)
    offer_ids = []
    true_signs = []

    for page in reader.pages:
        offer_ids.append(file.filename.split('.')[0])
        true_signs.append(page.extract_text())

    df = pd.DataFrame(
        {
            'offer_id': offer_ids,
            'true_sign': true_signs
        }
    )

    excel_data = io.BytesIO()
    df.to_excel(excel_data, index=False)
    excel_data.seek(0)
    return excel_data.getvalue()
    #towrite = io.BytesIO()
    #df.to_excel(towrite) 
    #towrite.seek(0)
    #return io.BytesIO(df.to_excel('true_signs.xlsx'))