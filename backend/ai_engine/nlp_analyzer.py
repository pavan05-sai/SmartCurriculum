# SmartCurriculum - NLP Analyzer
# Natural Language Processing for syllabus and job description analysis

import re
from typing import Dict, List, Optional
from collections import Counter


class NLPAnalyzer:
    """
    NLP analyzer for extracting topics and skills from text.
    
    Uses keyword extraction and pattern matching to analyze:
    - Course syllabi to identify topics and learning objectives
    - Job descriptions to extract required skills
    """
    
    def __init__(self):
        """Initialize the NLP analyzer with keyword databases."""
        self.skill_keywords = self._load_skill_keywords()
        self.topic_patterns = self._load_topic_patterns()
        self.stop_words = self._load_stop_words()
    
    def _load_skill_keywords(self) -> Dict[str, List[str]]:
        """
        Load skill keywords organized by category.
        These patterns help identify skills in text.
        """
        return {
            'programming_languages': [
                'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go',
                'rust', 'swift', 'kotlin', 'typescript', 'php', 'scala',
                'r programming', 'matlab'
            ],
            'web_technologies': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
                'django', 'flask', 'fastapi', 'spring', 'bootstrap', 'tailwind',
                'next.js', 'gatsby', 'graphql', 'rest api', 'websocket'
            ],
            'databases': [
                'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                'cassandra', 'dynamodb', 'oracle', 'sqlite', 'firebase',
                'database design', 'data modeling'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'data analysis', 'pandas',
                'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
                'data visualization', 'matplotlib', 'seaborn', 'tableau',
                'statistics', 'statistical analysis', 'a/b testing'
            ],
            'cloud_devops': [
                'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes',
                'jenkins', 'ci/cd', 'terraform', 'ansible', 'linux',
                'microservices', 'serverless', 'cloud computing'
            ],
            'tools': [
                'git', 'github', 'gitlab', 'jira', 'agile', 'scrum',
                'vs code', 'intellij', 'docker', 'postman'
            ],
            'concepts': [
                'data structures', 'algorithms', 'system design', 'design patterns',
                'object-oriented', 'oop', 'functional programming', 'api design',
                'software architecture', 'microservices', 'testing'
            ],
            'soft_skills': [
                'communication', 'teamwork', 'leadership', 'problem solving',
                'critical thinking', 'time management', 'collaboration'
            ]
        }
    
    def _load_topic_patterns(self) -> Dict[str, List[str]]:
        """
        Load patterns for identifying educational topics.
        """
        return {
            'introduction': [
                r'introduction to (\w+)',
                r'fundamentals of (\w+)',
                r'basics of (\w+)',
                r'getting started with (\w+)'
            ],
            'advanced': [
                r'advanced (\w+)',
                r'(\w+) advanced',
                r'deep dive into (\w+)'
            ],
            'practical': [
                r'(\w+) lab',
                r'hands-on (\w+)',
                r'practical (\w+)',
                r'(\w+) project'
            ]
        }
    
    def _load_stop_words(self) -> set:
        """Load common stop words to filter out."""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are',
            'were', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must',
            'shall', 'can', 'need', 'dare', 'ought', 'used', 'better',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'what', 'which', 'who', 'whom', 'whose', 'where',
            'when', 'why', 'how', 'all', 'each', 'every', 'both', 'few',
            'more', 'most', 'other', 'some', 'such', 'no', 'not', 'only',
            'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now'
        }
    
    def analyze_syllabus(self, syllabus_text: str) -> Dict:
        """
        Analyze course syllabus to extract topics and skills.
        
        Args:
            syllabus_text: The syllabus text to analyze
            
        Returns:
            Dictionary with extracted topics, skills, and structure
        """
        # Normalize text
        text = syllabus_text.lower()
        
        # Extract topics
        topics = self._extract_topics(syllabus_text)
        
        # Extract skills mentioned
        skills = self._extract_skills(text)
        
        # Identify learning objectives
        objectives = self._extract_objectives(syllabus_text)
        
        # Estimate course level
        level = self._estimate_level(text, topics)
        
        # Extract key concepts
        concepts = self._extract_key_concepts(text)
        
        # Detect prerequisites
        prerequisites = self._detect_prerequisites(text)
        
        return {
            'topics': topics,
            'skills': skills,
            'objectives': objectives,
            'level': level,
            'key_concepts': concepts,
            'prerequisites': prerequisites,
            'word_count': len(syllabus_text.split()),
            'summary': self._generate_summary(topics, skills, level)
        }
    
    def _extract_topics(self, text: str) -> List[Dict]:
        """Extract structured topics from syllabus text."""
        topics = []
        lines = text.split('\n')
        
        # Look for numbered or bulleted items
        topic_patterns = [
            r'^\s*(\d+[\.\)]\s*)(.+)',  # 1. Topic or 1) Topic
            r'^\s*([•\-\*]\s*)(.+)',     # Bullet points
            r'^(Unit|Module|Chapter|Week)\s*\d*[:.\s]*(.+)',  # Unit 1: Topic
        ]
        
        for line in lines:
            for pattern in topic_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    title = match.group(2).strip() if len(match.groups()) > 1 else match.group(1).strip()
                    if len(title) > 3 and title.lower() not in self.stop_words:
                        topics.append({
                            'title': title[:100],  # Limit length
                            'type': 'main_topic'
                        })
                    break
        
        # If no structured topics found, extract from text
        if not topics:
            topics = self._extract_topics_from_prose(text)
        
        return topics[:20]  # Limit to 20 topics
    
    def _extract_topics_from_prose(self, text: str) -> List[Dict]:
        """Extract topics from unstructured prose text."""
        topics = []
        
        # Use topic patterns to find mentions
        for category, patterns in self.topic_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = ' '.join(match)
                    topics.append({
                        'title': match.strip().title(),
                        'type': category
                    })
        
        return topics
    
    def _extract_skills(self, text: str) -> List[Dict]:
        """Extract skill mentions from text."""
        skills = []
        found_skills = set()
        
        for category, keywords in self.skill_keywords.items():
            for keyword in keywords:
                # Use word boundary matching
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text, re.IGNORECASE):
                    if keyword not in found_skills:
                        skills.append({
                            'name': keyword.title(),
                            'category': category
                        })
                        found_skills.add(keyword)
        
        return skills
    
    def _extract_objectives(self, text: str) -> List[str]:
        """Extract learning objectives from syllabus."""
        objectives = []
        
        # Look for objective markers
        objective_patterns = [
            r'students will (?:be able to |learn to )?(.+?)(?:\.|$)',
            r'(?:learn|understand|master|develop|create|build|analyze) (.+?)(?:\.|$)',
            r'by the end.+?(?:students will|you will) (.+?)(?:\.|$)',
            r'objective[s]?[:.\s]+(.+?)(?:\.|$)'
        ]
        
        for pattern in objective_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                objective = match.strip()
                if len(objective) > 10 and len(objective) < 200:
                    objectives.append(objective)
        
        return objectives[:10]  # Limit to 10 objectives
    
    def _estimate_level(self, text: str, topics: List[Dict]) -> str:
        """Estimate the course difficulty level."""
        advanced_keywords = ['advanced', 'complex', 'optimization', 'architecture', 'deep', 'expert']
        beginner_keywords = ['introduction', 'basic', 'fundamental', 'beginner', 'getting started', 'overview']
        
        text_lower = text.lower()
        
        advanced_count = sum(1 for kw in advanced_keywords if kw in text_lower)
        beginner_count = sum(1 for kw in beginner_keywords if kw in text_lower)
        
        if advanced_count > beginner_count + 2:
            return 'advanced'
        elif beginner_count > advanced_count + 2:
            return 'beginner'
        else:
            return 'intermediate'
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extract key technical concepts from text."""
        # Tokenize and count words
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        
        # Filter stop words and count
        filtered_words = [w for w in words if w not in self.stop_words]
        word_counts = Counter(filtered_words)
        
        # Return most common words that are likely concepts
        return [word for word, count in word_counts.most_common(15) if count > 1]
    
    def _detect_prerequisites(self, text: str) -> List[str]:
        """Detect course prerequisites mentioned in text."""
        prerequisites = []
        
        # Look for prerequisite markers
        prereq_pattern = r'prerequisite[s]?[:.\s]+(.+?)(?:\.|$|\n)'
        matches = re.findall(prereq_pattern, text, re.IGNORECASE)
        
        for match in matches:
            prerequisites.append(match.strip())
        
        # Also look for "prior knowledge of" or "familiarity with"
        prior_patterns = [
            r'prior knowledge of (.+?)(?:\.|$)',
            r'familiarity with (.+?)(?:\.|$)',
            r'background in (.+?)(?:\.|$)'
        ]
        
        for pattern in prior_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            prerequisites.extend([m.strip() for m in matches])
        
        return prerequisites[:5]
    
    def _generate_summary(self, topics: List[Dict], skills: List[Dict], level: str) -> str:
        """Generate a summary of the syllabus analysis."""
        topic_str = ', '.join([t['title'] for t in topics[:5]])
        skill_str = ', '.join([s['name'] for s in skills[:5]])
        
        return f"This {level}-level course covers topics including {topic_str}. " \
               f"Key skills developed: {skill_str}."
    
    def analyze_job_description(self, job_text: str) -> Dict:
        """
        Analyze job description to extract requirements.
        
        Args:
            job_text: The job description text
            
        Returns:
            Dictionary with extracted requirements and skills
        """
        text = job_text.lower()
        
        # Extract skills
        skills = self._extract_skills(text)
        
        # Categorize as required vs preferred
        required_skills = []
        preferred_skills = []
        
        # Look for requirement markers
        required_section = self._extract_section(job_text, ['required', 'must have', 'requirements', 'qualifications'])
        preferred_section = self._extract_section(job_text, ['preferred', 'nice to have', 'bonus', 'plus'])
        
        for skill in skills:
            skill_lower = skill['name'].lower()
            if skill_lower in required_section.lower():
                required_skills.append(skill['name'])
            elif skill_lower in preferred_section.lower():
                preferred_skills.append(skill['name'])
            else:
                # Default categorization based on context
                required_skills.append(skill['name'])
        
        # Extract experience requirements
        experience = self._extract_experience(text)
        
        # Extract education requirements
        education = self._extract_education(text)
        
        # Identify job level
        job_level = self._identify_job_level(text, experience)
        
        return {
            'required_skills': list(set(required_skills)),
            'preferred_skills': list(set(preferred_skills)),
            'all_skills': [s['name'] for s in skills],
            'experience': experience,
            'education': education,
            'job_level': job_level,
            'skill_categories': self._categorize_skills(skills)
        }
    
    def _extract_section(self, text: str, markers: List[str]) -> str:
        """Extract a section of text based on markers."""
        for marker in markers:
            pattern = rf'{marker}[:\s]*(.{{0,500}})'
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1)
        return text
    
    def _extract_experience(self, text: str) -> Dict:
        """Extract experience requirements from job description."""
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)(?:\s*of)?\s*(?:experience|exp)',
            r'experience[:\s]+(\d+)\+?\s*(?:years?|yrs?)',
            r'(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    return {
                        'min_years': int(match.group(1)),
                        'max_years': int(match.group(2))
                    }
                return {
                    'min_years': int(match.group(1)),
                    'max_years': None
                }
        
        return {'min_years': 0, 'max_years': None}
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education requirements."""
        education = []
        
        patterns = [
            r"bachelor'?s?\s*(?:degree)?(?:\s*in\s*[\w\s]+)?",
            r"master'?s?\s*(?:degree)?(?:\s*in\s*[\w\s]+)?",
            r'ph\.?d\.?',
            r'b\.?s\.?(?:\s*in\s*[\w\s]+)?',
            r'm\.?s\.?(?:\s*in\s*[\w\s]+)?',
            r'computer science',
            r'engineering'
        ]
        
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                match = re.search(pattern, text, re.IGNORECASE)
                education.append(match.group(0).strip())
        
        return list(set(education))
    
    def _identify_job_level(self, text: str, experience: Dict) -> str:
        """Identify the job level (entry, mid, senior, lead)."""
        text_lower = text.lower()
        min_years = experience.get('min_years', 0)
        
        if 'senior' in text_lower or 'lead' in text_lower or 'principal' in text_lower:
            return 'senior'
        elif 'junior' in text_lower or 'entry' in text_lower or min_years <= 1:
            return 'entry'
        elif min_years >= 5:
            return 'senior'
        elif min_years >= 3:
            return 'mid'
        else:
            return 'entry'
    
    def _categorize_skills(self, skills: List[Dict]) -> Dict[str, List[str]]:
        """Group skills by category."""
        categorized = {}
        for skill in skills:
            category = skill['category']
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(skill['name'])
        return categorized
    
    def match_syllabus_to_job(self, syllabus: str, job_description: str) -> Dict:
        """
        Match a syllabus against a job description.
        
        Returns:
            Match score and gap analysis
        """
        syllabus_analysis = self.analyze_syllabus(syllabus)
        job_analysis = self.analyze_job_description(job_description)
        
        # Get skills from both
        syllabus_skills = {s['name'].lower() for s in syllabus_analysis['skills']}
        required_skills = {s.lower() for s in job_analysis['required_skills']}
        
        # Calculate match
        matched = syllabus_skills.intersection(required_skills)
        missing = required_skills - syllabus_skills
        
        match_score = len(matched) / len(required_skills) * 100 if required_skills else 0
        
        return {
            'match_score': round(match_score, 1),
            'matched_skills': list(matched),
            'missing_skills': list(missing),
            'recommendation': 'Good alignment' if match_score >= 70 else 'Consider additional learning'
        }
