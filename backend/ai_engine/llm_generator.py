# SmartCurriculum - LLM Content Generator
# AI-powered content generation using LLM (with fallback templates)

import os
import json
from typing import Dict, List, Optional
from config import get_config


class LLMGenerator:
    """
    LLM-based content generator for educational materials.
    
    Generates:
    - Learning notes for topics
    - MCQs with explanations
    - Coding problems
    - Mini-project ideas
    - Resume bullet points
    
    Uses Anthropic Claude API when available, falls back to templates otherwise.
    """
    
    def __init__(self):
        """Initialize the LLM generator."""
        config = get_config()
        self.api_key = config.ANTHROPIC_API_KEY
        self.model = config.CLAUDE_MODEL
        self.use_api = bool(self.api_key)
        
        # Template database for fallback
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Load template database for fallback content generation."""
        return {
            'notes': {
                'Python Basics': '''
# Python Basics - Learning Notes

## Introduction
Python is a high-level, interpreted programming language known for its simplicity and readability.

## Key Concepts

### 1. Variables and Data Types
- Variables store data values
- Common types: int, float, str, bool, list, dict
- Dynamic typing - no need to declare types

```python
name = "Alice"  # string
age = 25        # integer
height = 5.6    # float
is_student = True  # boolean
```

### 2. Basic Operations
- Arithmetic: +, -, *, /, //, %, **
- Comparison: ==, !=, <, >, <=, >=
- Logical: and, or, not

### 3. Print and Input
```python
print("Hello, World!")
name = input("Enter your name: ")
```

## Practice Exercises
1. Create variables for your details
2. Perform basic calculations
3. Write a simple greeting program

## Summary
Python's simple syntax makes it ideal for beginners while being powerful enough for advanced applications.
''',
                'Data Structures': '''
# Data Structures - Learning Notes

## Introduction
Data structures are ways of organizing and storing data for efficient access and modification.

## Key Data Structures

### 1. Arrays/Lists
- Ordered collection of elements
- Index-based access (0-indexed)
- Dynamic size in Python

### 2. Stacks
- LIFO (Last In, First Out)
- Operations: push, pop, peek
- Use cases: undo operations, expression evaluation

### 3. Queues
- FIFO (First In, First Out)
- Operations: enqueue, dequeue
- Use cases: task scheduling, BFS

### 4. Hash Tables/Dictionaries
- Key-value pairs
- O(1) average lookup time
- Use cases: caching, counting

### 5. Trees
- Hierarchical structure
- Binary trees, BST, AVL trees
- Use cases: databases, file systems

## Time Complexity
| Operation | Array | Linked List | Hash Table |
|-----------|-------|-------------|------------|
| Access    | O(1)  | O(n)        | O(1)       |
| Search    | O(n)  | O(n)        | O(1)       |
| Insert    | O(n)  | O(1)        | O(1)       |

## Summary
Choosing the right data structure is crucial for algorithm efficiency.
'''
            },
            'mcqs': {
                'default': [
                    {
                        'question': 'What is the time complexity of accessing an element in an array by index?',
                        'options': ['O(1)', 'O(n)', 'O(log n)', 'O(n²)'],
                        'correct': 0,
                        'explanation': 'Array access by index is O(1) because elements are stored in contiguous memory locations.'
                    },
                    {
                        'question': 'Which data structure follows LIFO principle?',
                        'options': ['Queue', 'Stack', 'Linked List', 'Tree'],
                        'correct': 1,
                        'explanation': 'Stack follows Last In First Out (LIFO) principle where the last element added is the first one to be removed.'
                    },
                    {
                        'question': 'What is the primary advantage of using a hash table?',
                        'options': ['Ordered storage', 'O(1) average lookup', 'Memory efficiency', 'Simple implementation'],
                        'correct': 1,
                        'explanation': 'Hash tables provide O(1) average time complexity for lookup, insert, and delete operations.'
                    }
                ]
            },
            'projects': {
                'web_development': [
                    {
                        'title': 'Personal Portfolio Website',
                        'description': 'Build a responsive portfolio website showcasing your projects and skills.',
                        'skills': ['HTML', 'CSS', 'JavaScript', 'Responsive Design'],
                        'difficulty': 'beginner',
                        'estimated_hours': 10
                    },
                    {
                        'title': 'Task Management App',
                        'description': 'Create a full-stack task management application with user authentication.',
                        'skills': ['React', 'Node.js', 'MongoDB', 'REST APIs'],
                        'difficulty': 'intermediate',
                        'estimated_hours': 20
                    }
                ],
                'data_science': [
                    {
                        'title': 'Exploratory Data Analysis Project',
                        'description': 'Analyze a real-world dataset and create visualizations to derive insights.',
                        'skills': ['Python', 'Pandas', 'Matplotlib', 'Data Visualization'],
                        'difficulty': 'beginner',
                        'estimated_hours': 8
                    },
                    {
                        'title': 'Movie Recommendation System',
                        'description': 'Build a content-based or collaborative filtering recommendation system.',
                        'skills': ['Python', 'Scikit-learn', 'Machine Learning'],
                        'difficulty': 'intermediate',
                        'estimated_hours': 15
                    }
                ],
                'default': [
                    {
                        'title': 'CLI Application',
                        'description': 'Build a command-line application that solves a real problem.',
                        'skills': ['Programming', 'Problem Solving'],
                        'difficulty': 'beginner',
                        'estimated_hours': 8
                    }
                ]
            },
            'coding_problems': {
                'beginner': [
                    {
                        'title': 'Two Sum',
                        'description': 'Given an array of integers, return indices of two numbers that add up to a target.',
                        'difficulty': 'beginner',
                        'hints': ['Use a hash map for O(n) solution', 'Store complements as you iterate'],
                        'solution_approach': 'Use a dictionary to store numbers and their indices. For each number, check if its complement exists.'
                    },
                    {
                        'title': 'Reverse String',
                        'description': 'Write a function to reverse a string in-place.',
                        'difficulty': 'beginner',
                        'hints': ['Use two pointers', 'Swap characters from both ends'],
                        'solution_approach': 'Use two pointers at start and end, swap and move towards center.'
                    }
                ],
                'intermediate': [
                    {
                        'title': 'Valid Parentheses',
                        'description': 'Given a string containing brackets, determine if the input string is valid.',
                        'difficulty': 'intermediate',
                        'hints': ['Use a stack', 'Match opening and closing brackets'],
                        'solution_approach': 'Push opening brackets to stack, pop and match when encountering closing brackets.'
                    },
                    {
                        'title': 'Merge Two Sorted Lists',
                        'description': 'Merge two sorted linked lists into one sorted list.',
                        'difficulty': 'intermediate',
                        'hints': ['Use a dummy node', 'Compare and link nodes'],
                        'solution_approach': 'Create a dummy head, compare elements from both lists, and link smaller one.'
                    }
                ],
                'advanced': [
                    {
                        'title': 'LRU Cache',
                        'description': 'Design a data structure that follows LRU cache constraints.',
                        'difficulty': 'advanced',
                        'hints': ['Use hash map + doubly linked list', 'O(1) operations required'],
                        'solution_approach': 'Combine hash map for O(1) lookup with doubly linked list for O(1) removal/insertion.'
                    }
                ]
            }
        }
    
    def _call_claude(self, prompt: str) -> Optional[str]:
        """
        Call Anthropic Claude API to generate content.
        Returns None if API is not available or fails.
        """
        if not self.use_api or not self.model:
            return None
        
        try:
            from anthropic import Anthropic
            
            client = Anthropic(api_key=self.api_key)
            
            response = client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.7,
                system="You are an expert educational content creator. Generate clear, comprehensive, and engaging learning materials.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            if not response.content:
                return None
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Claude API error: {e}")
            return None
    
    def generate_notes(self, topic: str, detail_level: str = 'intermediate') -> Dict:
        """
        Generate learning notes for a topic.
        
        Args:
            topic: Topic title
            detail_level: 'basic', 'intermediate', or 'comprehensive'
            
        Returns:
            Dictionary with notes content and metadata
        """
        # Try API first
        if self.use_api:
            prompt = f"""Generate comprehensive learning notes for the topic: "{topic}"
            
Detail level: {detail_level}

Include:
1. Introduction and overview
2. Key concepts with explanations
3. Code examples (if applicable)
4. Practice exercises
5. Summary

Format in Markdown with proper headings and code blocks."""

            api_response = self._call_claude(prompt)
            if api_response:
                return {
                    'topic': topic,
                    'content': api_response,
                    'detail_level': detail_level,
                    'source': 'ai_generated'
                }
        
        # Fallback to templates
        template_key = None
        for key in self.templates['notes'].keys():
            if key.lower() in topic.lower() or topic.lower() in key.lower():
                template_key = key
                break
        
        if template_key:
            return {
                'topic': topic,
                'content': self.templates['notes'][template_key],
                'detail_level': detail_level,
                'source': 'template'
            }
        
        # Generate basic placeholder notes
        return {
            'topic': topic,
            'content': f"""# {topic} - Learning Notes

## Introduction
This topic covers the fundamentals and key concepts of {topic}.

## Key Concepts
1. Understanding the basics
2. Core principles and techniques
3. Practical applications

## Learning Objectives
- Understand the fundamental concepts
- Apply knowledge to solve problems
- Build practical skills

## Practice
Try implementing examples and working on exercises to reinforce learning.

## Summary
{topic} is an important skill that will help you in your career development.
""",
            'detail_level': detail_level,
            'source': 'generated'
        }
    
    def generate_mcqs(self, topic: str, count: int = 5, difficulty: str = 'intermediate') -> List[Dict]:
        """
        Generate multiple choice questions for a topic.
        
        Args:
            topic: Topic to generate questions for
            count: Number of questions to generate
            difficulty: 'beginner', 'intermediate', or 'advanced'
            
        Returns:
            List of MCQ dictionaries
        """
        # Try API first
        if self.use_api:
            prompt = f"""Generate {count} multiple choice questions for the topic: "{topic}"
            
Difficulty: {difficulty}

For each question provide:
1. Question text
2. 4 options (A, B, C, D)
3. Correct answer (0-3 index)
4. Brief explanation

Return as JSON array with format:
[{{"question": "...", "options": ["A", "B", "C", "D"], "correct": 0, "explanation": "..."}}]"""

            api_response = self._call_claude(prompt)
            if api_response:
                try:
                    # Try to parse JSON from response
                    # Handle case where response might have markdown code blocks
                    json_str = api_response.strip()
                    if json_str.startswith('```'):
                        json_str = json_str.split('```')[1]
                        if json_str.startswith('json'):
                            json_str = json_str[4:]
                    mcqs = json.loads(json_str)
                    return mcqs[:count]
                except json.JSONDecodeError:
                    pass
        
        # Fallback to templates
        template_mcqs = self.templates['mcqs'].get('default', [])
        
        # Generate topic-specific questions if possible
        mcqs = []
        for i in range(min(count, len(template_mcqs))):
            mcq = template_mcqs[i].copy()
            mcqs.append(mcq)
        
        # Fill remaining with generated questions
        while len(mcqs) < count:
            mcqs.append({
                'question': f'Question {len(mcqs) + 1} about {topic}',
                'options': ['Option A', 'Option B', 'Option C', 'Option D'],
                'correct': 0,
                'explanation': f'This tests your understanding of {topic}.'
            })
        
        return mcqs
    
    def generate_projects(self, topic: str, count: int = 3, difficulty: str = 'intermediate') -> List[Dict]:
        """
        Generate project ideas for a topic.
        
        Args:
            topic: Topic or skill area
            count: Number of projects to generate
            difficulty: 'beginner', 'intermediate', or 'advanced'
            
        Returns:
            List of project idea dictionaries
        """
        # Try API first
        if self.use_api:
            prompt = f"""Generate {count} mini-project ideas for learning: "{topic}"
            
Difficulty: {difficulty}

For each project provide:
1. Project title
2. Description (2-3 sentences)
3. Skills practiced
4. Estimated hours to complete
5. Key features to implement

Return as JSON array."""

            api_response = self._call_claude(prompt)
            if api_response:
                try:
                    json_str = api_response.strip()
                    if json_str.startswith('```'):
                        json_str = json_str.split('```')[1]
                        if json_str.startswith('json'):
                            json_str = json_str[4:]
                    projects = json.loads(json_str)
                    return projects[:count]
                except json.JSONDecodeError:
                    pass
        
        # Fallback to templates
        topic_lower = topic.lower()
        template_projects = self.templates['projects'].get('default', [])
        
        if 'web' in topic_lower or 'react' in topic_lower or 'javascript' in topic_lower:
            template_projects = self.templates['projects'].get('web_development', template_projects)
        elif 'data' in topic_lower or 'machine' in topic_lower or 'python' in topic_lower:
            template_projects = self.templates['projects'].get('data_science', template_projects)
        
        # Filter by difficulty and limit
        projects = [
            p for p in template_projects 
            if p.get('difficulty', 'intermediate') == difficulty or difficulty == 'intermediate'
        ][:count]
        
        # Fill remaining with generic projects
        while len(projects) < count:
            projects.append({
                'title': f'{topic} Practice Project {len(projects) + 1}',
                'description': f'Build a practical application applying {topic} concepts.',
                'skills': [topic],
                'difficulty': difficulty,
                'estimated_hours': 10
            })
        
        return projects
    
    def generate_coding_problems(
        self, 
        topic: str, 
        count: int = 3, 
        difficulty: str = 'intermediate',
        language: str = 'python'
    ) -> List[Dict]:
        """
        Generate coding problems for practice.
        
        Args:
            topic: Topic or concept
            count: Number of problems
            difficulty: 'beginner', 'intermediate', or 'advanced'
            language: Programming language for examples
            
        Returns:
            List of coding problem dictionaries
        """
        # Try API first
        if self.use_api:
            prompt = f"""Generate {count} coding problems for: "{topic}"
            
Difficulty: {difficulty}
Language: {language}

For each problem provide:
1. Problem title
2. Problem description
3. Hints (2-3)
4. Solution approach (without full code)
5. Example input/output

Return as JSON array."""

            api_response = self._call_claude(prompt)
            if api_response:
                try:
                    json_str = api_response.strip()
                    if json_str.startswith('```'):
                        json_str = json_str.split('```')[1]
                        if json_str.startswith('json'):
                            json_str = json_str[4:]
                    problems = json.loads(json_str)
                    return problems[:count]
                except json.JSONDecodeError:
                    pass
        
        # Fallback to templates
        template_problems = self.templates['coding_problems'].get(difficulty, [])
        problems = template_problems[:count]
        
        # Fill remaining
        while len(problems) < count:
            problems.append({
                'title': f'{topic} Challenge {len(problems) + 1}',
                'description': f'Implement a solution using {topic} concepts.',
                'difficulty': difficulty,
                'hints': ['Break down the problem', 'Consider edge cases'],
                'solution_approach': f'Apply {topic} principles systematically.'
            })
        
        return problems
    
    def generate_resume_bullet(self, skill_name: str, skill_level: str, style: str = 'impactful') -> str:
        """
        Generate a resume bullet point for a skill.
        
        Args:
            skill_name: Name of the skill
            skill_level: Proficiency level
            style: 'impactful', 'technical', or 'concise'
            
        Returns:
            Resume bullet point string
        """
        # Try API first
        if self.use_api:
            prompt = f"""Generate a single resume bullet point for the skill: "{skill_name}"
            
Proficiency level: {skill_level}
Style: {style}

The bullet should:
- Start with a strong action verb
- Be specific and quantifiable if possible
- Show impact or achievement
- Be 1-2 lines maximum

Return only the bullet point text, no other formatting."""

            api_response = self._call_claude(prompt)
            if api_response:
                return api_response.strip()
        
        # Fallback templates
        level_verbs = {
            'beginner': ['Gained foundational knowledge in', 'Learned fundamentals of', 'Developed basic skills in'],
            'intermediate': ['Applied', 'Utilized', 'Implemented solutions using', 'Developed applications with'],
            'advanced': ['Architected solutions using', 'Led development of projects with', 'Optimized systems using'],
            'expert': ['Mentored teams on', 'Designed enterprise-scale systems with', 'Pioneered adoption of']
        }
        
        import random
        verbs = level_verbs.get(skill_level, level_verbs['intermediate'])
        verb = random.choice(verbs)
        
        return f"{verb} {skill_name} to build efficient and scalable solutions"
    
    def generate_summary(self, content: str, max_length: int = 200) -> str:
        """
        Generate a summary of given content.
        
        Args:
            content: Text to summarize
            max_length: Maximum length of summary
            
        Returns:
            Summary string
        """
        if self.use_api:
            prompt = f"""Summarize the following content in {max_length} characters or less:

{content[:2000]}"""

            api_response = self._call_claude(prompt)
            if api_response:
                return api_response[:max_length]
        
        # Simple fallback - first sentences
        sentences = content.split('.')
        summary = ''
        for sentence in sentences:
            if len(summary) + len(sentence) < max_length:
                summary += sentence + '.'
            else:
                break
        
        return summary.strip() or content[:max_length]
