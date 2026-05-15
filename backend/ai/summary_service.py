from ai.chains import portfolio_chain
from ai_activity_logger import log_ai_activity

def generate_portfolio_summary(portfolio_results):

    try:

        response = portfolio_chain.invoke({
            "portfolio_data": str(portfolio_results)
        })
        log_ai_activity(
        str(portfolio_results),
        response.content
        )

        return response.content

    except Exception as e:

        return f"AI summary unavailable: {str(e)}"