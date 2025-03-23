# backend/prompt_engineering.py
from typing import Dict, Any

class PromptEngineer:
    """
    Handles the creation of sophisticated prompts for the Gemini model to generate
    platform-specific social media content.
    """
    
    # Platform-specific characteristics
    PLATFORM_CHARACTERISTICS = {
        "facebook": {
            "tone": "conversational, warm, and community-focused",
            "length": "medium to long (1-3 paragraphs)",
            "features": "can include questions, emojis, and calls for engagement",
            "audience": "diverse, friends and family connections",
            "content_types": "personal stories, updates, questions, celebrations, opinions"
        },
        "twitter": {
            "tone": "concise, witty, and often informal",
            "length": "short (under 280 characters)",
            "features": "hashtags, mentions, and brevity are important",
            "audience": "public, broader reach, topic-focused communities",
            "content_types": "breaking news, quick thoughts, jokes, trends, reactions"
        },
        "linkedin": {
            "tone": "professional, insightful, and industry-relevant",
            "length": "medium (1-2 paragraphs)",
            "features": "professional language, industry terms, occasional statistics",
            "audience": "professional connections, potential employers, industry peers",
            "content_types": "professional achievements, industry insights, career advice, company updates"
        }
    }
    
    @classmethod
    def create_prompt(cls, platform: str, user_input: str, additional_context: Dict[str, Any] = None) -> str:
        """
        Create a sophisticated prompt for the Gemini model.
        
        Args:
            platform: The target social media platform (facebook, twitter, linkedin)
            user_input: The user's original idea or content
            additional_context: Any additional context or requirements (optional)
            
        Returns:
            A detailed prompt for the Gemini model
        """
        platform = platform.lower()
        if platform not in cls.PLATFORM_CHARACTERISTICS:
            platform = "facebook"  
            
        platform_chars = cls.PLATFORM_CHARACTERISTICS[platform]
        prompt = f"""

You are an expert social media content creator specializing in {platform} content.

PLATFORM CHARACTERISTICS:
- Tone: {platform_chars['tone']}
- Length: {platform_chars['length']}
- Features: {platform_chars['features']}
- Audience: {platform_chars['audience']}
- Content Types: {platform_chars['content_types']}

USER'S IDEA:
{user_input}

ADDITIONAL REQUIREMENTS:
"""
        
        if platform == "facebook":
            prompt += """
- Create content that encourages engagement and conversation
- Include 1-2 relevant emojis where appropriate
- End with a question or call to action
- Keep paragraphs short and scannable
"""
        elif platform == "twitter":
            prompt += """
- Stick strictly to 280 characters or less
- Include 1-2 relevant hashtags if appropriate
- Use concise, impactful language
- Avoid unnecessary words or details
"""
        elif platform == "linkedin":
            prompt += """
- Begin with a professional hook or insight
- Include industry-relevant terminology
- Maintain a balance between informative and engaging
- End with a professional call to action or thought-provoking statement
- Avoid excessive use of emojis or informal language
"""
        prompt += """
- Generate content in the same language as the user's idea.
- Ensure the language and tone of the content align with the user's input language.
"""
        
        prompt += f"\n\nGenerate a single, ready-to-post {platform} content piece based on the user's idea and these guidelines."
        
        return prompt
