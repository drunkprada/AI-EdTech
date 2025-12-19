"""
Mock data generator for testing the EdTech UI without external API dependencies
"""

MOCK_DATA = {
    "Machine Learning": {
        "content": """
Machine learning is a method of data analysis that automates analytical model building. 
It is a branch of artificial intelligence based on the idea that systems can learn from 
data, identify patterns and make decisions with minimal human intervention. Deep learning 
is a subset of machine learning that uses neural networks with multiple layers to analyze 
various factors of data. Neural networks are computing systems inspired by the biological 
neural networks that constitute animal brains. Supervised learning is the machine learning 
task of learning a function that maps an input to an output based on example input-output 
pairs. Unsupervised learning is a type of machine learning that looks for previously 
undetected patterns in a data set with no pre-existing labels. Reinforcement learning 
is an area of machine learning concerned with how software agents ought to take actions 
in an environment in order to maximize the notion of cumulative reward. Feature engineering 
is the process of using domain knowledge to extract features from raw data via data mining 
techniques. Model training is the process of feeding a machine learning algorithm with data 
to help it learn. Overfitting occurs when a statistical model describes random error or 
noise instead of the underlying relationship. Cross-validation is a resampling method that 
uses different portions of the data to test and train a model on different iterations.
        """,
        "title": "Machine Learning"
    },
    "Quantum Physics": {
        "content": """
Quantum physics is the study of matter and energy at the most fundamental level. It aims 
to uncover the properties and behaviors of the very building blocks of nature. Wave-particle 
duality is the concept that every elementary particle exhibits the properties of both waves 
and particles. The Heisenberg uncertainty principle states that it is impossible to measure 
both the position and momentum of a particle with perfect accuracy at the same time. 
Quantum entanglement is a physical phenomenon that occurs when pairs or groups of particles 
interact in ways such that the quantum state of each particle cannot be described independently. 
Superposition is the ability of a quantum system to be in multiple states at the same time 
until it is measured. The Schrödinger equation is a mathematical equation that describes 
how the quantum state of a physical system changes over time. Quantum mechanics is the 
branch of physics that deals with the behavior of matter and light on the atomic and 
subatomic scale. The photoelectric effect is the emission of electrons when electromagnetic 
radiation hits a material. Quantum tunneling is a phenomenon where a particle passes through 
a potential barrier that it classically could not surmount.
        """,
        "title": "Quantum Physics"
    },
    "Renaissance Art": {
        "content": """
Renaissance art is the painting, sculpture and decorative arts of the period of European 
history known as the Renaissance. Renaissance art emerged in Italy around 1400 and spread 
throughout Europe during the 15th and 16th centuries. Perspective is a technique for 
representing three-dimensional objects on a two-dimensional surface. Humanism is a 
Renaissance cultural movement that turned away from medieval scholasticism and revived 
interest in ancient Greek and Roman thought. The High Renaissance was a period of artistic 
achievement that lasted from about 1490 to 1527. Leonardo da Vinci was an Italian polymath 
of the Renaissance whose areas of interest included invention, drawing, painting, sculpture, 
architecture, science, music, mathematics, engineering, literature, anatomy, geology, 
astronomy, botany, paleontology, and cartography. Michelangelo was an Italian sculptor, 
painter, architect and poet of the High Renaissance. Chiaroscuro is the use of strong 
contrasts between light and dark to achieve a sense of volume in modeling three-dimensional 
objects. Fresco is a technique of mural painting executed upon freshly laid lime plaster. 
The Sistine Chapel ceiling is a masterpiece of Renaissance art painted by Michelangelo.
        """,
        "title": "Renaissance Art"
    }
}

def get_mock_data(topic):
    """Get mock data for a topic"""
    # Check for exact match
    if topic in MOCK_DATA:
        return MOCK_DATA[topic]
    
    # Check for partial match
    for key in MOCK_DATA:
        if topic.lower() in key.lower() or key.lower() in topic.lower():
            return MOCK_DATA[key]
    
    # Default to Machine Learning
    return MOCK_DATA["Machine Learning"]
