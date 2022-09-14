from wave_function_package import *

class TextWaveHandler:
    """Manipulates text to work in the generic wave collapse function.
    
    Attributes
    ----------
    line_delimiter : str
        What string to split the input text by
    max_size : int
        What size to cap the wave function at
    radius : int
        What radius of interaction should be used by the wave collapse
    count_table : dict {<str> : dict {<str> : <int>} }
        Table for counting sub-strings by central character
    total_table : dict {<str> : int}
        Table for counting incidences of each character
    total_phonemes : int
        Total number of characters read from the input text
    patches_list : list <Patch>
        List of patches produced from the input text
    phoneme_list : list <str>
        List of unique characters read from the text
    word_start : int
        The value assigned to the starting character
    word_end : int
        The value assigned to the ending character
    wave : Wave
        The Wave object built to produce similar text to the input text
    padding_left : str
        The string used to pad the text to the left
    padding_right : str
        The string used to pad the text to the right
    """
    
    def __init__(self, line_delimiter = '\n',max_size=10,radius=1,padding_left="+",padding_right="-"):
        """    
        Parameters
        ----------
        line_delimiter : str
        max_size : int
        radius : int
        padding_left : str
        padding_right : str
        """
        
        self.line_delimiter = line_delimiter
        self.max_size = max_size
        self.radius = radius
        self.count_table = {}
        self.total_table = {}
        self.total_phonemes = 0
        self.patches_list = []
        self.phoneme_list = []
        self.word_start = 0
        self.word_end = 1
        self.padding_left = padding_left
        self.padding_right = padding_right
        self.wave = None
        
    def num_to_phoneme(self,num):
        """Converts from the wave's representation of a value to the original string.
        
        Parameters
        ----------
        num : int
            The value to convert
        
        Returns
        -------
        str
            The converted value
        """
        
        return self.phoneme_list[num]
    
    def phoneme_to_num(self,text):
        """Converts from the string of a value to the wave's numerical representation.
        
        Parameters
        ----------
        text : str
            The string to convert
        
        Returns
        -------
        int
            The converted value
        """
        
        return self.phoneme_list.index(text)
    
    def read_text(self,text):
        """Reads the input text and captures all values to generate the wave function super-position derived from it.
        
        Parameters
        ----------
        text : str
            The string to read
        """
        
        #Read text into tables of text
        words = text.split(self.line_delimiter)
        for word in words:
            padded_word = (self.padding_left*(self.radius+1)) + word + (self.padding_right*(self.radius+1))
            n = len(padded_word)
            for i in range(n - 2*self.radius):
                patch_text = padded_word[i:i+2*self.radius+1]
                phoneme = padded_word[i+self.radius]
                if phoneme not in self.phoneme_list:
                    self.phoneme_list.append(phoneme)
                    self.count_table[phoneme] = {}
                    self.total_table[phoneme] = 0
                if patch_text not in self.count_table[phoneme]:
                    self.count_table[phoneme][patch_text] = 0
                self.count_table[phoneme][patch_text] = self.count_table[phoneme][patch_text] + 1
                self.total_table[phoneme] = self.total_table[phoneme] + 1
                self.total_phonemes = self.total_phonemes + 1
        self.word_start = self.phoneme_list.index(self.padding_left)
        self.word_end = self.phoneme_list.index(self.padding_right)
        
        #turn tables of text in list of Patch objects for use in Wave()
        for phoneme in self.count_table:
            for patch_string in self.count_table[phoneme]:
                raw_patch = [self.phoneme_to_num(c) for c in patch_string]
                p = Patch(self.phoneme_to_num(phoneme), raw_patch, self.radius, self.count_table[phoneme][patch_string])
                self.patches_list.append(p)
                
    def generate_wave(self):
        """Creates the Wave object.
        """
        
        self.wave = Wave(self.radius, self.max_size, self.word_start, self.word_end, self.patches_list)

    def print_wave_raw(self):
        """Prints the contents of the collapsed wave as text.
        """
        
        out = ""
        for we in self.wave.waveform:
            out = out + self.num_to_phoneme(we.selected_core)
        
        print(out.strip("+-"))
        
    def mid_print(self):
        """Prints some contents of the wave function while it isn't collapsed.
        """
        
        out = "\n"
        for we in self.wave.waveform:
            var = "[" + ''.join( self.num_to_phoneme(k) for k in we.possible_cores) \
                + "|" + ((str(we.selected_core) + "|") if we.collapsed else "") + str(we.collapsed) + "]"
            out = out + var + "\n"
        print(out)

    def produce(self, n, max_out = 2000):
        """Produces random strings from the wave function collapse.
        
        Parameters
        ----------
        n : int
            The number of random strings to produce
        max_out : int, optional
            The maximum number of attempts to make before ending prematurely
        
        Returns
        -------
        int
            The converted value
        """
        
        i = 0
        while i < n:
            max_out = max_out - 1
            if max_out < 0:
                print("maxed out production loops")
                break
            self.generate_wave()
            success = self.wave.collapse()
            if success:
                self.print_wave_raw()
                i = i+1
            