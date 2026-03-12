# SmartCurriculum - Major Domain Curriculum Datasets
# Uses academic_structure.json for detailed topics

import json
import os

# Load academic structure
def load_academic_structure():
    """Load the academic structure JSON file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'academic_structure.json')
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except:
        return {}

ACADEMIC_STRUCTURE = load_academic_structure()

# Domain configurations with semester mappings
DOMAIN_CONFIGS = {
    "engineering-cs": {
        "title": "B.Tech Computer Science & Engineering",
        "domain": "Engineering",
        "department": "Computer Science",
        "program_type": "B.Tech",
        "total_semesters": 8,
        "difficulty": "intermediate"
    },
    "engineering-ece": {
        "title": "B.Tech Electronics & Communication",
        "domain": "Engineering", 
        "department": "Electronics",
        "program_type": "B.Tech",
        "total_semesters": 8,
        "difficulty": "intermediate"
    },
    "engineering-mech": {
        "title": "B.Tech Mechanical Engineering",
        "domain": "Engineering",
        "department": "Mechanical",
        "program_type": "B.Tech",
        "total_semesters": 8,
        "difficulty": "intermediate"
    },
    "engineering-civil": {
        "title": "B.Tech Civil Engineering",
        "domain": "Engineering",
        "department": "Civil",
        "program_type": "B.Tech",
        "total_semesters": 8,
        "difficulty": "intermediate"
    },
    "science-physics": {
        "title": "B.Sc Physics",
        "domain": "Science",
        "department": "Physics",
        "program_type": "B.Sc",
        "total_semesters": 6,
        "difficulty": "intermediate"
    },
    "science-chemistry": {
        "title": "B.Sc Chemistry",
        "domain": "Science",
        "department": "Chemistry",
        "program_type": "B.Sc",
        "total_semesters": 6,
        "difficulty": "intermediate"
    },
    "science-math": {
        "title": "B.Sc Mathematics",
        "domain": "Science",
        "department": "Mathematics",
        "program_type": "B.Sc",
        "total_semesters": 6,
        "difficulty": "intermediate"
    },
    "science-biology": {
        "title": "B.Sc Biology",
        "domain": "Science",
        "department": "Biology",
        "program_type": "B.Sc",
        "total_semesters": 6,
        "difficulty": "intermediate"
    },
    "medical-mbbs": {
        "title": "MBBS",
        "domain": "Medical",
        "department": "Human Anatomy",
        "program_type": "MBBS",
        "total_semesters": 10,
        "difficulty": "advanced"
    },
    "medical-pharma": {
        "title": "B.Pharma",
        "domain": "Medical",
        "department": "Pharmacology",
        "program_type": "B.Pharma",
        "total_semesters": 8,
        "difficulty": "intermediate"
    },
    "commerce-bcom": {
        "title": "B.Com",
        "domain": "Commerce",
        "department": "Business Administration",
        "program_type": "B.Com",
        "total_semesters": 6,
        "difficulty": "intermediate"
    },
    "commerce-bba": {
        "title": "BBA",
        "domain": "Commerce",
        "department": "Business Administration",
        "program_type": "BBA",
        "total_semesters": 6,
        "difficulty": "intermediate"
    },
    "commerce-mba": {
        "title": "MBA",
        "domain": "Commerce",
        "department": "Finance",
        "program_type": "MBA",
        "total_semesters": 4,
        "difficulty": "advanced"
    },
    "law-llb": {
        "title": "LLB",
        "domain": "Law",
        "department": "Law",
        "program_type": "LLB",
        "total_semesters": 6,
        "difficulty": "intermediate"
    },
    "law-ballb": {
        "title": "BA LLB (Integrated)",
        "domain": "Law",
        "department": "Law",
        "program_type": "BA LLB",
        "total_semesters": 10,
        "difficulty": "intermediate"
    },
    "arts-economics": {
        "title": "BA Economics",
        "domain": "Arts & Humanities",
        "department": "Economics",
        "program_type": "BA",
        "total_semesters": 6,
        "difficulty": "intermediate"
    },
    "arts-psychology": {
        "title": "BA Psychology",
        "domain": "Arts & Humanities",
        "department": "Psychology",
        "program_type": "BA",
        "total_semesters": 6,
        "difficulty": "intermediate"
    },
    "arts-english": {
        "title": "BA English Literature",
        "domain": "Arts & Humanities",
        "department": "English Literature",
        "program_type": "BA",
        "total_semesters": 6,
        "difficulty": "intermediate"
    },
    "bca": {
        "title": "BCA",
        "domain": "Engineering",
        "department": "Computer Science",
        "program_type": "BCA",
        "total_semesters": 6,
        "difficulty": "beginner"
    },
    "mca": {
        "title": "MCA",
        "domain": "Engineering",
        "department": "Computer Science",
        "program_type": "MCA",
        "total_semesters": 4,
        "difficulty": "advanced"
    }
}


def get_curriculum_for_domain(domain_id):
    """Generate semester-wise curriculum for a domain."""
    config = DOMAIN_CONFIGS.get(domain_id, DOMAIN_CONFIGS["engineering-cs"])
    
    # Get topics from academic structure
    domain_data = ACADEMIC_STRUCTURE.get(config["domain"], {})
    dept_data = domain_data.get("departments", {}).get(config["department"], {})
    topics = dept_data.get("topics", [])
    
    # Distribute topics across semesters
    total_semesters = config["total_semesters"]
    topics_per_sem = max(1, len(topics) // total_semesters) if topics else 3
    
    semesters = []
    topic_idx = 0
    
    for sem_num in range(1, total_semesters + 1):
        subjects = []
        
        # Add topics from academic structure
        for i in range(topics_per_sem):
            if topic_idx < len(topics):
                topic = topics[topic_idx]
                subjects.append({
                    "code": f"{config['department'][:2].upper()}{sem_num}0{i+1}",
                    "title": topic["title"],
                    "credits": 4 if topic.get("type") == "core" else 3,
                    "hours_lecture": 3,
                    "hours_lab": 2 if topic.get("type") != "elective" else 0,
                    "description": topic.get("description", ""),
                    "skills": topic.get("skills_gained", [])
                })
                topic_idx += 1
        
        # Add common subjects based on semester
        if sem_num == 1:
            subjects.extend([
                {"code": "MA101", "title": "Mathematics I", "credits": 4, "hours_lecture": 4, "hours_lab": 0, "description": "Calculus and linear algebra", "skills": ["Mathematics"]},
                {"code": "HU101", "title": "Communication Skills", "credits": 2, "hours_lecture": 2, "hours_lab": 0, "description": "Technical writing and presentation", "skills": ["Communication"]}
            ])
        elif sem_num == 2:
            subjects.append({"code": "EV101", "title": "Environmental Studies", "credits": 2, "hours_lecture": 2, "hours_lab": 0, "description": "Environmental awareness", "skills": ["Environment"]})
        elif sem_num == total_semesters:
            subjects.extend([
                {"code": "PR801", "title": "Major Project", "credits": 6, "hours_lecture": 0, "hours_lab": 12, "description": "Final year project", "skills": ["Project Development"]},
                {"code": "IN801", "title": "Internship", "credits": 4, "hours_lecture": 0, "hours_lab": 0, "description": "Industry internship", "skills": ["Industry Experience"]}
            ])
        
        credits_total = sum(s.get("credits", 3) for s in subjects)
        
        semesters.append({
            "semester": sem_num,
            "name": f"Semester {sem_num}",
            "credits_total": credits_total,
            "subjects": subjects
        })
    
    return {
        "title": config["title"],
        "description": f"{config['program_type']} program in {config['department']}",
        "program_type": config["program_type"],
        "total_semesters": total_semesters,
        "total_credits": sum(s["credits_total"] for s in semesters),
        "difficulty": config["difficulty"],
        "semesters": semesters
    }


def get_all_domains():
    """Get list of all available domains grouped by category."""
    domains = []
    for domain_id, config in DOMAIN_CONFIGS.items():
        domains.append({
            "id": domain_id,
            "name": config["title"],
            "category": config["domain"],
            "program_type": config["program_type"],
            "total_semesters": config["total_semesters"],
            "difficulty": config["difficulty"]
        })
    return domains


def get_domains_by_category():
    """Get domains organized by major category."""
    categories = {}
    for domain_id, config in DOMAIN_CONFIGS.items():
        cat = config["domain"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append({
            "id": domain_id,
            "name": config["title"],
            "program_type": config["program_type"]
        })
    return categories
