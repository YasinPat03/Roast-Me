import { Image, StyleSheet, Platform,Pressable,Text,SafeAreaView} from 'react-native';

import { HelloWave } from '@/components/HelloWave';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

export default function HomeScreen() {
  return (
<SafeAreaView><Pressable style={styles.button}>
      <Text style={styles.text}>Roast Me!</Text>
    </Pressable></SafeAreaView>
    
  );
}

const styles = StyleSheet.create({
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  stepContainer: {
    gap: 8,
    marginBottom: 8,
  },
  reactLogo: {
    height: 178,
    width: 290,
    bottom: 0,
    left: 0,
    position: 'absolute',
  },
  text:{
    color:"black",
  },
  button:{
    width:50,
    height:20,
    backgroundColor:"white",
    justifyContent:"center",
    alignItems:"center",
    display:"flex",
  }
});
