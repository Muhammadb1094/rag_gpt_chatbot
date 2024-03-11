from .utils import (read_data_from_pdf, get_text_chunks, get_embedding,
                    create_qdrant_collection, add_points_qdrant)
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from langchain.vectorstores import Qdrant
from langchain.embeddings import OpenAIEmbeddings



class UploadPdfView(APIView):
   
    def post(self, request):
        all_pdf = [
                    'documents/HubSpot_Certification_Study_Guide_2014_pro_ent.pdf',
                    'documents/hubspot-ebook_river-pools-blogging-case-study.pdf',
                    'documents/impromptu-rh.pdf',
                    'documents/small-business-social-media-ebook-hubspot.pdf'
                ]
        
        for pdf_path in all_pdf:
            pdf_name = pdf_path.split('/')[-1].split('.')[0]

            try:
                print("Creating Collection for: ", pdf_name)
                create_qdrant_collection(pdf_name)
            except Exception as e:
                return Response({"message": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            pdf_content = read_data_from_pdf(pdf_path)
            content_chunks = get_text_chunks(pdf_content)
            
            print("Creating Embeddins for: ", pdf_name)
            embaddings_points = get_embedding(content_chunks)
            
            print("Adding Embeddins for: ", pdf_name)
            add_points_qdrant(pdf_name, embaddings_points)
                            
        return Response({"message": "PDF uploaded successfully"},
                         status=status.HTTP_200_OK)
    


