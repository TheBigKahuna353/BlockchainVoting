from core.Block import VoteBlock

class VotingSystem:

    def __init__(self):
        self.votes = {}

    def calulate_votes(self, chain):
        """
        A function to calculate the votes from the chain.
        This function will be called by a node whenever the user wants to see the current vote count.
        """
        for block in chain:
            if not isinstance(block, VoteBlock): continue
            self.add_vote(block.data['vote'])
            
    def add_vote(self, vote):
        if vote in self.votes:
            self.votes[vote] += 1
        else:
            self.votes[vote] = 1

    def get_votes(self):
        return self.votes

    def get_vote_count(self):
        return len([x for x in self.votes.values()])

    def get_vote_count_for_candidate(self, candidate):
        return self.votes[candidate]

    def get_winner(self):
        return max(self.votes, key=self.votes.get)