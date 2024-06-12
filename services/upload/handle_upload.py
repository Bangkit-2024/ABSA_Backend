import pandas as pd
from django.db import transaction
from content.models import Review, RealReviewAspectSentiment, Company

def is_content_valid(df: pd.DataFrame, ignore_empty=False)->bool:
    """Check if header and content correct

    Args:
        df (pd.DataFrame): Dataframe

    Returns:
        bool: Return true if condition is true
        Criterion :
        -   There should be a header_name for review_text
        -   If ignore args on There should not be a empty dataset
    """ 
    isColumnRight = {'review_text','company'}.issubset(df.columns)
    isNotEmpty = not df.isna().any().iloc[0] 



    return isColumnRight and ( ignore_empty or isNotEmpty )
    

    
def is_header_include_absa(df:pd.DataFrame)->bool:
    """Check if input data include aspect and sentiment data

    Args:
        df (pd.DataFrame): 

    Returns:
        bool: Will be true if there is aspect and setiment column in the file
    """
    return {'aspect','sentiment'}.issubset(df.columns)

def handle_bulk_aspect_based_review(request,df:pd.DataFrame):
    
    with transaction.atomic():
        for _,row in df.iterrows():
            review = Review(
            review_text = row['review_text'],
            company = Company.objects.filter(id=row['company']).first()
            )
            review.save()

            review_absa = RealReviewAspectSentiment(
                review = review,
                aspect = row['aspect'],
                sentiment = row['sentiment'],
                user=request.user
            )

            review_absa.save()

def handle_bulk_review_only(request,df:pd.DataFrame):
    
    Review.objects.bulk_create(
        [ Review(review_text=row['review_text'], company=Company.objects.filter(id=row['company']).first())
                 for _,row in df.iterrows()]
    )

