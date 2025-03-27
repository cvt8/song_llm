import math
from itertools import combinations

class MusicEvaluator:
    def __init__(self, alpha=1.0, beta=1.0, t_ref=480):
        """
        Initialize evaluator with hyperparameters
        alpha: sensitivity for duration consistency
        beta: sensitivity for time intervals
        t_ref: reference duration (default 480 = quarter note in MIDI ticks)
        """
        self.alpha = alpha
        self.beta = beta
        self.t_ref = t_ref
        
        # Harmonic weights based on your specification
        self.interval_weights = {
            0: 0.0,   # Octave
            7: 0.1,   # Fifth
            5: 0.1,   # Fifth (complement)
            3: 0.2,   # Third major/minor
            4: 0.2,
            8: 0.2,
            9: 0.2,
            1: 0.6,   # Second/seventh
            2: 0.6,
            10: 0.6,
            11: 0.6,
            6: 0.8    # Triton
        }

    def parse_notes(self, note_sequence):
        """Parse input string into list of note dictionaries"""
        notes = []
        for note in note_sequence.split():
            p, v, d, t = note.split(':')
            notes.append({
                'pitch': int(p[1:]),
                'velocity': int(v[1:]),
                'duration': int(d[1:]),
                'time': int(t[1:])
            })
        return notes

    def harmonic_score(self, chord_pitches):
        """Calculate harmonic score for a set of pitches"""
        if len(chord_pitches) < 2:
            return 1.0  # Single note is perfectly consonant
        
        total_score = 0
        pairs = 0
        
        for p1, p2 in combinations(chord_pitches, 2):
            interval = min(abs(p1 - p2) % 12, 12 - abs(p1 - p2) % 12)
            # Default to 0.4 for unspecified intervals
            dissonance = self.interval_weights.get(interval, 0.4)
            total_score += 1.0 - dissonance  # Convert dissonance to consonance
            pairs += 1
            
        return total_score / pairs if pairs > 0 else 1.0

    def duration_score(self, duration):
        """Calculate duration consistency score"""
        ratio = duration / self.t_ref
        j = round(math.log2(ratio))
        diff = abs(math.log2(ratio) - j)
        return math.exp(-self.alpha * diff)

    def time_score(self, time_interval):
        """Calculate time interval score"""
        if time_interval == 0:  # Simultaneous notes
            return 1.0
        ratio = time_interval / self.t_ref
        j = round(math.log2(ratio))
        diff = abs(math.log2(ratio) - j)
        return math.exp(-self.beta * diff)

    def evaluate(self, note_sequence):
        """Main evaluation function"""
        notes = self.parse_notes(note_sequence)
        
        # Group notes by time for harmonic evaluation
        time_groups = {}
        prev_time = 0
        absolute_time = 0
        
        for note in notes:
            absolute_time += note['time']
            if absolute_time not in time_groups:
                time_groups[absolute_time] = []
            time_groups[absolute_time].append(note['pitch'])

        # Calculate scores
        harmonic_scores = []
        duration_scores = []
        time_scores = []
        
        # Process harmonic scores for each time group
        for time in time_groups:
            harmonic_scores.append(self.harmonic_score(time_groups[time]))
        
        # Process duration and time scores
        for i, note in enumerate(notes):
            duration_scores.append(self.duration_score(note['duration']))
            if i > 0:
                time_interval = notes[i]['time']
                time_scores.append(self.time_score(time_interval))

        # Calculate average scores
        h_avg = sum(harmonic_scores) / len(harmonic_scores) if harmonic_scores else 1.0
        d_avg = sum(duration_scores) / len(duration_scores) if duration_scores else 1.0
        t_avg = sum(time_scores) / len(time_scores) if time_scores else 1.0

        # Final score: weighted average normalized to 20
        # Giving equal weight to harmony (50%) and rhythm (25% each)
        final_score = (0.5 * h_avg + 0.25 * d_avg + 0.25 * t_avg) * 20
        
        return {
            'total_score': round(final_score, 2),
            'harmonic_score': round(h_avg * 10, 2),  # Out of 10
            'duration_score': round(d_avg * 5, 2),   # Out of 5
            'time_score': round(t_avg * 5, 2)        # Out of 5
        }

# Example usage
if __name__ == "__main__":
    evaluator = MusicEvaluator(alpha=1.0, beta=1.0, t_ref=480)
    
    # Test sequence
    test_sequence = "p54:v95:d960:t0 p56:v94:d960:t0 p61:v93:d480:t480"
    
    result = evaluator.evaluate(test_sequence)
    print(f"Music Evaluation Results:")
    print(f"Total Score: {result['total_score']}/20")
    print(f"Harmonic Score: {result['harmonic_score']}/10")
    print(f"Duration Score: {result['duration_score']}/5")
    print(f"Time Score: {result['time_score']}/5")