class Patch:
    """Represents a single sub-string for purpose of wave-collapse.
    
    Attributes
    ----------
    core : int
        The central element of the sub-string
    raw_patch : list <int>
        The complete list of elements of the sub-string
    radius : int
        The radius of the sub-string, or the number of elements to one side of the core
    length : int
        The length of the sub-string
    frequency : int
        The number of occurences of this sub-string within the base text
        """
    
    def __init__(self, core, raw_patch, radius, frequency = 1):
        """
        Parameters
        ----------
        core : int
            The central element of the sub-string
        raw_patch : list <int>
            The complete list of elements of the sub-string
        radius : int
            The radius of the sub-string, or the number of elements to one side of the core
        frequency : int, optional
            The number of occurences of this sub-string within the base text
        """
        
        self.core = core
        self.raw_patch = raw_patch
        self.radius = radius
        self.length = 2*radius + 1
        self.frequency = frequency
        
    def set_frequency(self, frequency):
        """
        Parameters
        ----------
        frequency : int
            The number of occurences of this sub-string within the base text
        """
        
        self.frequency = frequency
        
    def add_frequency(self, increment):
        """
        Parameters
        ----------
        frequency : int
            The number of new occurences to add of this sub-string within the base text
        """
        
        self.frequency = self.frequency + increment
        
    def same_pattern(self, other):
        """
        Parameters
        ----------
        other : Patch
            Check if the patterns represented are the same between this Patch and another
        """
        
        return self.core == other.core and self.raw_patch == other.raw_patch 
    
    def match_surroundings(self, surroundings):
        """Check if this Patch could exist at the center of the possible wave surrounding it.
        
        Parameters
        ----------
        surroundings : list <WaveElement>
            The possible wave surrounding this patch.
        
        Returns
        -------
        bool
            If this Patch could exist at the center of the surroundings.
            
        """
        
        for i in range(self.radius):
            #Invalid if any element of the patch is not possible in the corresponding location in the surroundings
            if self.raw_patch[i] not in surroundings[i].possible_cores:
                return False
            if self.raw_patch[-1-i] not in surroundings[-1-i].possible_cores:
                return False
        return True