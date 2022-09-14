import random
import math
from wave_function_package import Patch
from wave_function_package import WaveElement

class Wave:
    """Represents a complete wave function in super-position.
    
    Attributes
    ----------
    waveform : list <WaveElement>
        The current state of the wave function
    patches_list : list <Patch>
        Every possible Patch
    radius : int
        The radius of interaction and Patches 
    max_size : int
        The maximum length of the wave function
    word_start_core : int
        The core value that will represent the start of the wave
    word_end_core : int
        The core value that will represent the end of the wave
    success : bool
        If the wave collapsed into a valid state
    worst_quality : int
        The highest value for quality of an element in the wave
    """
    
    def __init__(self, radius, max_size, word_start_core, word_end_core, patches_list):
        """
        Parameters
        ----------
        radius : int
        max_size : int
        word_start_core : int
        word_end_core : int
        patches_list : list <Patch>
        """
        
        self.waveform = []
        self.patches_list = patches_list
        self.radius = radius
        self.max_size = max_size
        self.word_start_core = word_start_core
        self.word_end_core = word_end_core
        self.populate()
        self.success = True
        self.worst_quality = 0
        
    def populate(self):
        """Generates the complete super-position of the wave and populates it with WaveElements
        """
        
        self.waveform = [ WaveElement(self.patches_list) for i in range(2*self.radius + self.max_size)]
        self.worst_quality = self.waveform[0].get_collapse_quality()
        for i in range(self.radius):
            self.waveform[i].fixed_collapse(self.word_start_core)
            self.waveform[-1-i].fixed_collapse(self.word_end_core)
            
    def seed_collapse(self):
        """Chooses a random index of the wave and collapses it to begin the wave function collapse.
        
        Returns
        -------
        int
            The index of the element collapsed
        """
        
        index = random.randint(0,self.max_size-1)
        self.waveform[self.radius + index].probable_collapse()
        return index
    
    def do_best_collapse(self):
        """Find and collapse the best possible WaveElement

        Returns
        -------
        int
            The index of the element collapsed
        """
        
        best_quality = self.worst_quality *2 + 1000
        i_list = []
        for i in range(len(self.waveform)):
            if not self.waveform[i].collapsed:
                if self.waveform[i].get_collapse_quality() < best_quality:
                    best_quality = self.waveform[i].get_collapse_quality()
                    i_list = [i]
                elif self.waveform[i].get_collapse_quality() == best_quality:
                    i_list.append(i)
        i = random.choice(i_list)
        self.waveform[i].probable_collapse()
        return i
    
    def cull_at(self,index):
        """Removes invalid Patches from the selected WaveElement, bringing it closer to collapse.
        
        Parameters
        ----------
        index : int
            The index of the WaveElement to cull
        
        Returns
        -------
        bool
            If the cull changed anything
        """
        
        if not self.waveform[index].collapsed:
            wave_selection = self.waveform[index-self.radius:index+self.radius+1]
            return self.waveform[index].cull_patches(wave_selection)
        return
    
    def empty_propogate(self):
        """Scans over the wave and culls WaveElements based on their neighbors.
        """
        
        max_cycles = 1
        for cycle in range(max_cycles):
            changed = False
            for i in range(self.max_size):
                j = self.radius + i
                changed = changed or self.cull_at(j)
            for i in range(self.max_size):
                j = self.radius + self.max_size - i -1
                changed = changed or self.cull_at(j)
            if not changed:
                break
    def propogate_from(self, index):
        """Scans over the surroundings of a WaveElement and culls its neighbors, then the whole wave.
        
        Parameters
        ----------
        index : int
            The index of the WaveElement to cull around
        """
        l = len(self.waveform)
        
        
        for i in range(self.radius):
            right_index = index + i + 1
            left_index = index - i - 1
            if right_index - self.radius >= 0 and right_index + self.radius < l:
                self.cull_at(right_index)
            if left_index - self.radius >= 0 and left_index + self.radius < l:
                self.cull_at(left_index)
        
        self.empty_propogate()
        
        
    def check_fully_collapsed(self):
        """Check if every element of the wave is collapsed.
        
        Returns
        -------
        bool
            If every element of the wave is collapsed
        """
        
        full_collapse = True
        for w in self.waveform:
            full_collapse = full_collapse and w.check_collapse()
        return full_collapse
    
    def check_failed_collapse(self):
        """Check if the collapse has failed to resolve correctly.
        
        This wave function collapse algorithm does not guarantee correct results,
        as that is the domain of quantum computing. Instead, it can easily identify 
        when it has reached a dead-end wave and restarts.
        
        Returns
        -------
        bool
            If the wave collapse failed
        """
        
        failed = False
        for w in self.waveform:
            failed = failed or len(w.possible_cores) == 0
        return failed
    
    def collapse(self):
        """Collapses the wave from its super-position completely

        Returns
        -------
        bool
            If the collapse was successful
        """
        
        i = self.seed_collapse()
        self.propogate_from(i)
        
        
        while not (self.check_fully_collapsed() or self.check_failed_collapse()):
            self.empty_propogate()
            if self.check_failed_collapse():
                break
            self.propogate_from(self.do_best_collapse())
        self.empty_propogate()
        return not self.check_failed_collapse()