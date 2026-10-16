/* ft_probe.c - load a font as named instance #1 and render 'A' via FreeType.
 * Mirrors EchoChat: FT_New_Memory_Face -> FT_Set_Named_Instance(1)
 *                   -> FT_Set_Char_Size(12ppem) -> FT_Load_Glyph(char 'A').
 * Build against FreeType 2.13.0 (+ASAN) to confirm the CVE-2025-27363 OOB fires.
 */
#include <stdio.h>
#include <stdlib.h>
#include <ft2build.h>
#include FT_FREETYPE_H
#include FT_MULTIPLE_MASTERS_H

int main(int argc, char** argv){
  if(argc<2){ fprintf(stderr,"usage: %s font.ttf [charcode=0x41]\n",argv[0]); return 2; }
  unsigned long cc = (argc>=3)? strtoul(argv[2],0,0) : 0x41;
  FILE* f=fopen(argv[1],"rb"); if(!f){perror("open");return 2;}
  fseek(f,0,SEEK_END); long n=ftell(f); fseek(f,0,SEEK_SET);
  unsigned char* buf=malloc(n); fread(buf,1,n,f); fclose(f);

  FT_Library lib; FT_Init_FreeType(&lib);
  FT_Face face; FT_Error e;
  e=FT_New_Memory_Face(lib,buf,n,0,&face);
  printf("FT_New_Memory_Face=0x%x num_glyphs=%ld face_index=0x%lx\n",
         e, e?-1:(long)face->num_glyphs, e?0:(long)face->face_index);
  if(e) return 1;

  e=FT_Set_Named_Instance(face,1);
  printf("FT_Set_Named_Instance(1)=0x%x face_index(after)=0x%lx IS_NAMED_INSTANCE=%d\n",
         e,(long)face->face_index, (int)((face->face_index & 0x7FFF0000L)!=0));

  FT_Set_Char_Size(face,0,12*64,72,72);
  FT_UInt gi=FT_Get_Char_Index(face, cc);
  printf("char 0x%lx -> glyph index %u ; loading...\n", cc, gi);
  fflush(stdout);
  e=FT_Load_Glyph(face, gi, 0);
  printf("FT_Load_Glyph=0x%x  (if you see this with ASAN silent, no OOB fired)\n", e);

  FT_Done_Face(face); FT_Done_FreeType(lib); free(buf);
  return 0;
}
